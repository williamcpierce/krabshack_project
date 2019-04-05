from django.shortcuts import render, redirect
import esi_app.esi as esi
from .models import EsiCharacter


def login(request):
    # view for new character auth, redirects to auth url if user is logged in
    if request.user.is_authenticated:
        token = esi.generate_token()
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
    # passing user id for use in retrieving character portrait
    if request.user.is_authenticated:
        uid = request.user.social_auth.get(provider='eveonline').uid
        esicharacters = EsiCharacter.objects.filter(assoc_user=request.user)
        lpdict = {}
        lpsum = 0
        # loops over all characters belonging to logged in user
        for character in esicharacters:
            lp = 0
            # gets lp values
            esi.esi_security.update_token(character.get_sso_data())
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
            # stores updated tokens
            tokens = esi.esi_security.refresh()
            character.update_token(tokens)
        return render(
            request,
            'esi_app/esilp.html',  {
                'lpdict': lpdict,
                'lpsum': lpsum,
                'uid': uid
            }
        )
    else:
        return render(request, 'esi_app/esilp.html')
