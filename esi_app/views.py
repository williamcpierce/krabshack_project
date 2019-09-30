from django.conf import settings
from django.shortcuts import render, redirect
from .models import EsiCharacter
from site_app.models import LPRate
import esi_app.esi as esi
import esi_app.util as util
import sys
import requests


def login(request):
    """
    view for new character auth, redirects to auth url if user is logged in
    """
    if request.user.is_authenticated:

        # generates csrf token
        csrf_token = util.generate_token()

        # writes csrf token to session
        request.session['csrf_token'] = csrf_token
        return redirect(
            esi.esi_security.get_auth_uri(
                state=csrf_token,
                scopes=['esi-characters.read_loyalty.v1']
            )
        )

    else:
        return redirect('/')


def callback(request):
    """
    catches redirects from auth, exchanges code for auth/refresh tokens, creates model object
    """
    # verifies csrf token
    state_token = request.GET.get('state')
    session_token = request.session.pop('csrf_token', None)
    if session_token is None or state_token is None or state_token != session_token:
        print("Ah ah ah, you didn't say the magic word!", file=sys.stderr)
        return redirect('/')

    # gets code from login process
    auth_code = request.GET.get('code')

    # retreives tokens
    auth_response = esi.esi_security.auth(auth_code)

    # retreives character information
    character_data = esi.esi_security.verify()

    # instantializes active character
    esi_character = EsiCharacter()
    esi_character.character_id = character_data['sub'].split(':')[2]
    esi_character.character_owner_hash = character_data['owner']
    esi_character.character_name = character_data['name']
    esi_character.assoc_user = request.user

    # passes character to method to update tokens and write to db
    esi_character.update_tokens(auth_response)

    # passes character to method to make esi call
    esi_character.update_data()
    
    return redirect('/')


def esilp(request):
    """
    for each character associated with the logged in user, pulls name and lp values
    """
    # gets lp values
    guristas_lp_rate = LPRate.objects.get(lp_type='Guristas').lp_rate
    sanshas_lp_rate = LPRate.objects.get(lp_type='Sanshas').lp_rate

    # initializing variables
    lp_dict = {}
    guristas_lp_sum = 0
    sanshas_lp_sum = 0
    guristas_lp_value = 0
    sanshas_lp_value = 0

    # checks if user is logged in and/or is a superuser
    if request.user.is_authenticated:
        if request.user.is_superuser:
            esi_characters = EsiCharacter.objects.all()
        else:
            esi_characters = EsiCharacter.objects.filter(assoc_user=request.user)

        # loops over characters
        for character in esi_characters:

            # gives security object the character's tokens
            esi_data = character.get_tokens()
            esi.esi_security.update_token(esi_data)
            
            try:
                # refreshes and stores tokens/updates data if expired
                if esi_data['expires_in'] < 0:
                    esi_tokens = esi.esi_security.refresh()
                    character.update_tokens(esi_tokens)
                    character.update_data()
            except:
                sanshas_lp = 'ESI Error'
                guristas_lp = 'ESI Error'
            else:
                # parses esi data
                all_lp = character.character_lp
                guristas_lp = util.parse_lp(all_lp, 1000127)
                sanshas_lp = util.parse_lp(all_lp, 1000161) + util.parse_lp(all_lp, 1000162)

            # builds dictionary of lp values for each character
            owner = character.assoc_user.username
            lp_dict[character.character_name] = [
                guristas_lp,
                sanshas_lp,
                owner
            ]

            # calculates lp sums, skipped if value is not an integer
            if isinstance(guristas_lp, int):
                guristas_lp_sum = guristas_lp_sum + guristas_lp
            if isinstance(sanshas_lp, int):
                sanshas_lp_sum = sanshas_lp_sum + sanshas_lp

        # calculates lp values 
        guristas_lp_value = guristas_lp_rate * guristas_lp_sum
        sanshas_lp_value = sanshas_lp_rate * sanshas_lp_sum

    return render(
        request,
        'esi_app/esilp.html', {
            'lp_dict': lp_dict,
            'guristas_lp_rate': guristas_lp_rate,
            'guristas_lp_sum': guristas_lp_sum,
            'guristas_lp_value': guristas_lp_value,
            'sanshas_lp_rate': sanshas_lp_rate,
            'sanshas_lp_sum': sanshas_lp_sum,
            'sanshas_lp_value': sanshas_lp_value
        }
    )
