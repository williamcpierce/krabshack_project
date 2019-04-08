from django.shortcuts import render, redirect
import esi_app.esi as esi
from .models import EsiCharacter
import sys


def login(request):
    # view for new character auth, redirects to auth url if user is logged in
    if request.user.is_authenticated:
        # generates csrf token
        token = esi.generate_token()
        # writes csrf token to session
        request.session['token'] = token
        return redirect(esi.esi_security.get_auth_uri(
            state=token,
            scopes=['esi-characters.read_loyalty.v1']
        ))
    else:
        return redirect('/')


def callback(request):
    # catches redirects from auth, exchanges code for auth/refresh tokens, creates model object
    # gets code from login process
    code = request.GET.get('code')
    # verifies csrf token
    token = request.GET.get('state')
    sess_token = request.session.pop('token', None)
    if sess_token is None or token is None or token != sess_token:
        print("u dun goofed", file=sys.stderr)
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
    esicharacter.assoc_user = request.user.username
    # passes character to method to update tokens and write to db
    esicharacter.update_token(auth_response)
    return redirect('/')


def esilp(request):
    # for each character associated with the logged in user, pulls name and guristas lp
    if request.user.is_authenticated:
        esicharacters = EsiCharacter.objects.filter(assoc_user=request.user)
        lpdict = {}
        lpsum = 0
        # loops over all characters belonging to logged in user
        for character in esicharacters:
            lp = 0
            # gives security object tokens
            sso_data = character.get_sso_data()
            esi.esi_security.update_token(sso_data)
            # gets lp values
            op = esi.esi_app.op['get_characters_character_id_loyalty_points'](
                character_id=character.character_id
            )
            all_lp = esi.esi_client.request(op)
            # gets guristas lp amount
            for item in all_lp.data:
                if item.get('corporation_id') == 1000127:
                    lp = item.get('loyalty_points')
                    break
            # builds dictionary of lp values for each character
            name = character.character_name
            lpdict[name] = lp
            # sum all user lp
            lpsum = lpsum + lp
            # refreshes and stores tokens if expired
            print(sso_data['expires_in'], file=sys.stderr)
            if sso_data['expires_in'] < 0:
                tokens = esi.esi_security.refresh()
                character.update_token(tokens)
        return render(
            request,
            'esi_app/esilp.html',  {
                'lpdict': lpdict,
                'lpsum': lpsum
            }
        )
    else:
        return render(request, 'esi_app/esilp.html')
