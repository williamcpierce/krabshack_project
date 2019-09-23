from django.conf import settings
from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect
import esi_app.esi as esi
from .models import EsiCharacter
from site_app.models import Rates
# from .forms import CashoutForm
# from datetime import datetime, timezone
import sys
import requests


def login(request):
    """view for new character auth, redirects to auth url if user is logged in"""
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
    """catches redirects from auth, exchanges code for auth/refresh tokens, creates model object"""
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
    """for each character associated with the logged in user, pulls name and guristas lp"""
    # get buyback rate
    # with requests.Session() as s:
    #     download = s.get(settings.CSV_URL)
    #     decode = download.content.decode('utf-8')
    #     lprate = int(''.join(list(filter(str.isdigit, decode))))
    guristas_lprate = Rates.objects.get(lp_type="Guristas").lp_rate
    sanshas_lprate = Rates.objects.get(lp_type="Sanshas").lp_rate
    if request.user.is_authenticated:
        if request.user.is_superuser:
            esicharacters = EsiCharacter.objects.all()
        else:
            esicharacters = EsiCharacter.objects.filter(assoc_user=request.user)
        # initialize/reset variables
        lpdict = {}
        guristas_lpsum = 0
        sanshas_lpsum = 0
        # loops over all characters belonging to logged in user
        for character in esicharacters:
            # initialize/reset variables
            guristas_lp = 0
            truecreations_lp = 0
            truepower_lp = 0
            sanshas_lp = 0
            # gives security object tokens
            sso_data = character.get_sso_data()
            esi.esi_security.update_token(sso_data)
            # gets lp values, error handling if this fails
            op = esi.esi_app.op['get_characters_character_id_loyalty_points'](
                character_id=character.character_id
            )
            # parses esi response
            try:
                all_lp = esi.esi_client.request(op)
                # gets guristas lp amount
                for item in all_lp.data:
                    if item.get('corporation_id') == 1000127:
                        guristas_lp = item.get('loyalty_points')
                # gets true creations lp amount
                    if item.get('corporation_id') == 1000161:
                        truecreations_lp = item.get('loyalty_points')
                # gets true power lp amount
                    if item.get('corporation_id') == 1000162:
                        truepower_lp = item.get('loyalty_points')
                sanshas_lp = truecreations_lp + truepower_lp
            except:
                guristas_lp = "ESI Error"
                sanshas_lp = "ESI Error"
            # builds dictionary of lp values for each character
            name = character.character_name
            lpdict[name] = [guristas_lp, sanshas_lp]
            # sum all user lp
            try:
                if guristas_lpsum == "N/A":
                    guristas_lpsum = "N/A"
                else:
                    guristas_lpsum = guristas_lpsum + guristas_lp
                if sanshas_lpsum == "N/A":
                    sanshas_lpsum = "N/A"
                else:
                    sanshas_lpsum = sanshas_lpsum + sanshas_lp
            except:
                guristas_lpsum = "N/A"
                sanshas_lpsum = "N/A"
            # refreshes and stores tokens if expired
            try:
                if sso_data['expires_in'] < 0:
                    tokens = esi.esi_security.refresh()
                    character.update_token(tokens)
            except:
                lp = 0
        # get user lp value
        if guristas_lpsum == "N/A" or guristas_lp == "ESI Error":
            guristas_lpvalue = "N/A"
        else:
            guristas_lpvalue = guristas_lpsum * guristas_lprate
        if sanshas_lpsum == "N/A" or sanshas_lp == "ESI Error":
            sanshas_lpvalue = "N/A"
        else:
            sanshas_lpvalue = sanshas_lpsum * guristas_lprate
        return render(
            request,
            'esi_app/esilp.html',  {
                'lpdict': lpdict,
                'guristas_lpsum': guristas_lpsum,
                'sanshas_lpsum': sanshas_lpsum,
                'guristas_lprate': guristas_lprate,
                'sanshas_lprate': sanshas_lprate,
                'guristas_lpvalue': guristas_lpvalue,
                'sanshas_lpvalue': sanshas_lpvalue
            }
        )
    else:
        return render(
            request,
            'esi_app/esilp.html',  {
                'guristas_lprate': guristas_lprate,
                'sanshas_lprate': sanshas_lprate
            }
        )


# def cashout(request):
#    if request.method == 'POST':
#        form = CashoutForm(request.POST)
#        if form.is_valid():
#            cashout = form.save(commit=False)
#            cashout.requester = request.user
#            cashout.request_date = datetime.now(timezone.utc)
#            cashout.save()
#            return redirect('/')
#
#    else:
#        form = CashoutForm()
#
#    return render(request, 'esi_app/cashout.html', {'form': form})
