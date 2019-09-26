from django.conf import settings
from django.shortcuts import render, redirect
from .models import EsiCharacter
from site_app.models import LPRate
import esi_app.esi as esi
import sys
import requests


def login(request):
    """view for new character auth, redirects to auth url if user is logged in"""
    if request.user.is_authenticated:

        # generates csrf token
        token = esi.generate_token()

        # writes csrf token to session
        request.session['token'] = token
        return redirect(
            esi.esi_security.get_auth_uri(
                state=token,
                scopes=['esi-characters.read_loyalty.v1']
            )
        )

    else:
        return redirect('/')


def callback(request):
    """catches redirects from auth, exchanges code for auth/refresh tokens, creates model object"""
    # gets code from login process
    code = request.GET.get('code')

    # verifies csrf token
    token = request.GET.get('state')
    sess_token = request.session.pop('token', None)
    if sess_token is None or token is None or token != sess_token:
        print("Ah ah ah, you didn't say the magic word!", file=sys.stderr)
        return redirect('/')

    # retreives tokens
    auth_response = esi.esi_security.auth(code)

    # retreives character information
    cdata = esi.esi_security.verify()

    # instantializes active character
    esicharacter = EsiCharacter()
    esicharacter.character_id = cdata['sub'].split(':')[2]
    esicharacter.character_owner_hash = cdata['owner']
    esicharacter.character_name = cdata['name']
    esicharacter.assoc_user = request.user

    # passes character to method to update tokens and write to db
    esicharacter.update_token(auth_response)
    
    return redirect('/')


def esilp(request):
    """for each character associated with the logged in user, pulls name and guristas lp"""
    # gets lp values
    guristas_lprate = LPRate.objects.get(lp_type="Guristas").lp_rate
    sanshas_lprate = LPRate.objects.get(lp_type="Sanshas").lp_rate

    # initializing variables
    lpdict = {}
    guristas_lpsum = 0
    sanshas_lpsum = 0
    guristas_lpvalue = 0
    sanshas_lpvalue = 0

    # checks if user is logged in and/or is a superuser
    if request.user.is_authenticated:
        if request.user.is_superuser:
            esicharacters = EsiCharacter.objects.all()
        else:
            esicharacters = EsiCharacter.objects.filter(assoc_user=request.user)

        # loops over characters
        for character in esicharacters:
            
            # initializing variables
            guristas_lp = 0
            tc_lp = 0
            tp_lp = 0
            sanshas_lp = 0

            # gives security object the character's tokens
            esi_data = character.get_esi_data()
            esi.esi_security.update_token(esi_data)

            
            try:
                # refreshes and stores tokens/updates data if expired
                if esi_data['expires_in'] < 0:
                    tokens = esi.esi_security.refresh()
                    character.update_token(tokens)

                # parses esi data
                all_lp = character.character_lp
                for item in all_lp:
                    if item.get("corporation_id") == 1000127:
                        guristas_lp = item.get("loyalty_points")
                        break
                    else:
                        guristas_lp = 0
                for item in all_lp:
                    if item.get("corporation_id") == 1000161:
                        tc_lp = item.get("loyalty_points")
                        break
                    else:
                        tc_lp = 0
                for item in all_lp:
                    if item.get("corporation_id") == 1000162:
                        tp_lp = item.get("loyalty_points")
                        break
                    else:
                        tp_lp = 0
                sanshas_lp = tc_lp + tp_lp
            except:
                sanshas_lp = "ESI Error"
                guristas_lp = "ESI Error"

            # builds dictionary of lp values for each character
            owner = character.assoc_user.username
            lpdict[character.character_name] = [
                guristas_lp,
                sanshas_lp,
                owner
            ]

            # calculates lp sums, skipped if value is not an integer
            if isinstance(guristas_lp, int):
                guristas_lpsum = guristas_lpsum + guristas_lp
            if isinstance(sanshas_lp, int):
                sanshas_lpsum = sanshas_lpsum + sanshas_lp

        # calculates lp values 
        guristas_lpvalue = guristas_lprate * guristas_lpsum
        sanshas_lpvalue = sanshas_lprate * sanshas_lpsum


    return render(
        request,
        'esi_app/esilp.html', {
            'lpdict': lpdict,
            'guristas_lprate': guristas_lprate,
            'guristas_lpsum': guristas_lpsum,
            'guristas_lpvalue': guristas_lpvalue,
            'sanshas_lprate': sanshas_lprate,
            'sanshas_lpsum': sanshas_lpsum,
            'sanshas_lpvalue': sanshas_lpvalue
        }
    )
