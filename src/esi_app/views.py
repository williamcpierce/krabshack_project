from datetime import datetime, timedelta, timezone
from json import dumps
import sys

from django.conf import settings
from django.shortcuts import redirect, render
import esi_app.util as util
import requests

from .esi import esi_app, esi_client, esi_security
from .models import EsiCharacter, EsiMarket
from .moon import moon
from site_app.models import LPRate



def login(request):
    """View for new character auth, redirects to auth url if user is logged in."""

    if request.user.is_authenticated:

        # Generates csrf token
        csrf_token = util.generate_token()

        # Checks if user is in VG
        character_id = request.user.social_auth.get().uid
        if util.get_corp(character_id) == 98477766:
            scopes=[
                'esi-characters.read_loyalty.v1',
                'esi-bookmarks.read_character_bookmarks.v1',
                'esi-universe.read_structures.v1',
                'esi-search.search_structures.v1'
            ]
        else:
            scopes=['esi-characters.read_loyalty.v1']

        # Writes csrf token to session
        request.session['csrf_token'] = csrf_token
        return redirect(
            esi_security.get_auth_uri(
                state=csrf_token,
                scopes=scopes
            )
        )

    else:
        return redirect('/')


def callback(request):
    """Catches redirects from auth, exchanges code for auth/refresh tokens, creates model object."""

    # Verifies csrf token
    state_token = request.GET.get('state')
    session_token = request.session.pop('csrf_token', None)
    if session_token is None or state_token is None or state_token != session_token:
        print("Ah ah ah, you didn't say the magic word!", file=sys.stderr)
        return redirect('/')

    # Gets code from login process
    auth_code = request.GET.get('code')

    # Retreives tokens
    auth_response = esi_security.auth(auth_code)

    # Retreives character information
    character_data = esi_security.verify()

    # Instantializes active character
    esi_character = EsiCharacter()
    esi_character.character_id = character_data['sub'].split(':')[2]
    esi_character.character_owner_hash = character_data['owner']
    esi_character.character_name = character_data['name']
    esi_character.assoc_user = request.user

    # Passes character to method to update tokens and write to db
    esi_character.update_tokens(auth_response)

    # Passes character to method to make esi call
    esi_character.update_lp()

    return redirect('/')


def esilp(request):
    """For each character associated with the logged in user, pulls name and lp values."""

    # Initializing variables
    lp_dict = {}
    lp_summary_dict = {}
    guristas_lp_sum = 0
    sanshas_lp_sum = 0
    ded_lp_sum = 0
    esi_error = {'status': False}

    # Gets lp values
    guristas_lp_rate = LPRate.objects.get(lp_type='Guristas').lp_rate
    sanshas_lp_rate = LPRate.objects.get(lp_type='Sanshas').lp_rate
    ded_lp_rate = LPRate.objects.get(lp_type='DED').lp_rate

    # Checks if user is logged in and/or is a superuser
    if request.user.is_authenticated:
        if request.user.is_superuser:
            esi_characters = EsiCharacter.objects.all()
        else:
            esi_characters = EsiCharacter.objects.filter(assoc_user=request.user)

        # Loops over characters
        for character in esi_characters:

            # Gives security object the character's tokens
            esi_data = character.get_tokens()
            esi_security.update_token(esi_data)

            try:
                # Refreshes and stores tokens/updates data if expired
                if esi_data['expires_in'] < 0:
                    esi_tokens = esi_security.refresh()
                    character.update_tokens(esi_tokens)
                    character.update_lp()
            except:
                sanshas_lp = 'ESI Error'
                guristas_lp = 'ESI Error'
                ded_lp = 'ESI Error'
                esi_error = {
                    'status': True,
                    'title': 'ESI Error',
                    'body': (
                        'An error has occurred.\n' \
                        'One or more of your character authorizations may have become invalid.\n' \
                        'Please re-add the affected character(s) to resolve this error.'
                    )
                }

            else:
                # Parses esi data
                all_lp = character.character_lp
                guristas_lp = util.parse_lp(all_lp, 1000127)
                sanshas_lp = util.parse_lp(all_lp, 1000161) + util.parse_lp(all_lp, 1000162)
                ded_lp = util.parse_lp(all_lp, 1000137)

            # Builds dictionary of lp values for each character
            owner = character.assoc_user.username
            lp_dict[character.character_name] = [
                guristas_lp,
                sanshas_lp,
                ded_lp,
                owner
            ]

            # Calculates lp sums, skipped if value is not an integer
            if isinstance(guristas_lp, int):
                guristas_lp_sum += guristas_lp
            if isinstance(sanshas_lp, int):
                sanshas_lp_sum += sanshas_lp
            if isinstance(ded_lp, int):
                ded_lp_sum += ded_lp

        # Stores lp sums and rates
        lp_summary_dict['guristas_lp_sum'] = guristas_lp_sum
        lp_summary_dict['sanshas_lp_sum'] = sanshas_lp_sum
        lp_summary_dict['ded_lp_sum'] = ded_lp_sum
        lp_summary_dict['guristas_lp_rate'] = guristas_lp_rate
        lp_summary_dict['sanshas_lp_rate'] = sanshas_lp_rate
        lp_summary_dict['ded_lp_rate'] = ded_lp_rate

        # Calculates and stores lp values
        lp_summary_dict['guristas_lp_value'] = guristas_lp_rate * guristas_lp_sum
        lp_summary_dict['sanshas_lp_value'] = sanshas_lp_rate * sanshas_lp_sum
        lp_summary_dict['ded_lp_value'] = ded_lp_rate * ded_lp_sum

    return render(
        request,
        'esi_app/esilp.html', {
            'lp_dict': lp_dict,
            'lp_summary_dict': lp_summary_dict,
            'error': esi_error,
            'subheader': 'LP Data'
        }
    )


def esimarket(request):
    """Pulls all saved items that are redeemable in lp stores."""

    # Hides non-LP items unless superuser
    if request.user.is_superuser:
        items = EsiMarket.objects.all()
    else:
        items = EsiMarket.objects.exclude(lp_type='None')

    # Gets datetime of the most recent update
    orders_last_updated = EsiMarket.objects.latest('orders_last_updated').orders_last_updated

    # Disallow refresh if orders were updated in hhe last hour
    if orders_last_updated < datetime.now(timezone.utc)-timedelta(hours=1):
        disable_refresh = False
    else:
        disable_refresh = True

    return render(
        request,
        'esi_app/esimarket.html', {
            'items': items,
            'last_updated': orders_last_updated,
            'subheader': 'Market Data',
            'refreshable': True,
            'disable_refresh': disable_refresh
        }
    )


def esimarketupdate(request):
    # Doesn't update non-LP items unless superuser
    if request.user.is_superuser:
        items = EsiMarket.objects.all()
    else:
        items = EsiMarket.objects.exclude(lp_type='None')

    # Updates values if expired
    for item in items:
        item.update_orders()

    return redirect('/esi/market')


def esimoon(request):
    # Checks if user is in VG or superuser
    character_id = request.user.social_auth.get().uid
    if util.get_corp(character_id) == 98477766 or request.user.is_superuser:

        # Initializing variables
        moon_times_dict = {}

        # Shows all for superuser
        if request.user.is_superuser:
            esi_characters = EsiCharacter.objects.all()
        else:
            esi_characters = EsiCharacter.objects.filter(assoc_user=request.user)

        # Loops over characters
        for character in esi_characters:

            # Gives security object the character's tokens
            esi_data = character.get_tokens()
            esi_security.update_token(esi_data)

            # Refreshes and stores tokens/updates data if expired
            if esi_data['expires_in'] < 0:
                esi_tokens = esi_security.refresh()
                character.update_tokens(esi_tokens)

            # Calculates and stores moon pop times
            try:
                moon_times_dict = moon(character, moon_times_dict)
            except:
                moon_times_dict = moon_times_dict

        return render(
            request,
            'esi_app/esimoon.html', {
                'moon_times_dict': moon_times_dict,
                'subheader': 'Moon Data'
            }
        )
    else:
        return redirect('/')
