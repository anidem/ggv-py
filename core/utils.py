# utils.py
import csv
import codecs
import cStringIO
from datetime import datetime

from openpyxl import Workbook
from openpyxl.cell import get_column_letter
from openpyxl.styles import Font

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect

from social.exceptions import SocialAuthBaseException, AuthException, AuthForbidden

from .models import ActivityLog


class GGVExcelWriter:


    wb = None

    def __init__(self):
        self.wb = Workbook()

    def write_row(self, ws, data=[]):
        ws.append(data)

    def save(self, f):
        self.wb.save(f)

    # def write_row_1(self, ws, u):
    #     ws.append(['GEDid', 'users name', 'users email', datetime.now()])
    #     ws.append([])  # Blank row
    #     for i in self.USER_INFO_CELLS:
    #         ws[i].font = Font(size=16, name='Arial')

    # def setup_data_cols(self, ws):
    #     for col_num in xrange(len(self.DATA_COLS)):
    #         offset = col_num+1
    #         cell = ws.cell(row=3, column=offset)
    #         cell.value = self.DATA_COLS[col_num][1]
    #         cell.font = Font(size=14, name='Arial')
    #         # set column width
    #         ws.column_dimensions[self.DATA_COLS[col_num][0]].width = self.DATA_COLS[col_num][2]

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding. Needed for unicode in csv
    writer.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def logout_clean(request):
    ActivityLog(user=request.user, action='logout', message='user logged out').save()
    logout(request)

    return redirect('https://accounts.google.com/Logout?&continue=https://www.google.com')


class GGVAuthForbidden(SocialAuthBaseException):
    """Auth process exception."""
    def __init__(self, backend, response, gaccount, *args, **kwargs):
        self.backend = backend
        self.gaccount = gaccount
        self.response = response
        super(GGVAuthForbidden, self).__init__(*args, **kwargs)

    def __str__(self):
        m = 'The google account in use in this browser ' + self.gaccount + ' is not allowed on this site. Please see instructions below. '
        return m


def auth_allowed(response, details, *args, **kwargs):
    """
    Return the ggv user object if authenticated email matches a user email.
    Implies that allowed users must be created in system beforehand, with an
    email that matches the gmail account used to authenticate.
    """
    try:
        ggv_user = User.objects.get(username=details.get('email'))
        return ggv_user
    except:
        return None


def ggv_auth_allowed(backend, details, response, *args, **kwargs):
    """
    If auth_allowed returns a user object, set the user variable for the pipeline.
    A valid user variable is processed to determine if a social (google) association needs
    to be created. See ggv_social for the next op in the pipeline.
    """
    ggv_user = auth_allowed(response, details)
    if not ggv_user:
        raise GGVAuthForbidden(backend, response, details['username'])
    else:
        return {'user': ggv_user}


def ggv_social_user(backend, uid, user=None, *args, **kwargs):
    """
    Previous pipeline op, ggv_auth_allowed, should prevent a null user but
    checking here, again, just in case.
    The effect of this op is that a social association is set. If social association
    is None, the pipeline will create a new social association to the ggv user object.
    Subsequent (non overridden pipeline ops) will process as designed, based on the social and user
    variables being initialized with values.
    """
    if user:
        provider = backend.name
        social = backend.strategy.storage.user.get_social_auth(provider, uid)
        if not social:  # user has not logged in previously (e.g., no social auth obj exists) -- make their account active.
            user.is_active = True
    else:
        raise AuthForbidden(backend)

    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}
