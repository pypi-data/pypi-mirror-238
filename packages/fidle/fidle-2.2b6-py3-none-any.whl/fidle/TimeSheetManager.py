# ------------------------------------------------------------------
#       _______ _                 _____ _               _   
#      |__   __(_)               / ____| |             | |  
#         | |   _ _ __ ___   ___| (___ | |__   ___  ___| |_ 
#         | |  | | '_ ` _ \ / _ \\___ \| '_ \ / _ \/ _ \ __|
#         | |  | | | | | | |  __/____) | | | |  __/  __/ |_ 
#         |_|  |_|_| |_| |_|\___|_____/|_| |_|\___|\___|\__|
#
#                                            fidle.TimeSheetManager         
# ------------------------------------------------------------------
#     
# A simple class to manage time sheets.
# Jean-Luc Parouty CNRS/MIAI/SIMaP 2022



import os,platform,sys
import json
import datetime, time
import dateutil
import pathlib
import base64
import hashlib
from random  import uniform
from string import Template
import yaml
import re

from IPython.display import display
import pandas as pd

from email.header         import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
import email
import imaplib
import smtplib
import fidle.utils


import fidle.config
from fidle.Chrono import Chrono


class TimeSheetManager:

    __version__  = fidle.config.VERSION


    def __read_profile(self, profile_path):
        '''
        Load profile
        args:
            profile_name : path to the yaml profile file
        return:
            profile
        '''
        # ---- Profile 
        profile_path =  os.path.expanduser(profile_path)
        with open(profile_path,'r') as fp:
            profile=yaml.load(fp, Loader=yaml.FullLoader)

        # ---- Events
        active_events = profile['active_events']
        events = dict()
    
        for events_dir in active_events:

            # ---- Read events file
            #
            events_file = f'{events_dir}/events.yml'
            events_file =  os.path.expanduser(events_file)
            with open(events_file,'r') as fp:
                content = yaml.load(fp, Loader=yaml.FullLoader)
            events_list   = content['events']
            events_config = content['config']

            # ---- Add events to list
            #
            for (id,event) in events_list.items():
                # Get a copy of event global config
                full_event = events_config.copy()
                # Add event infos
                full_event.update(event)
                # Add label, config path, convert duration to int
                full_event['label']      = events_config['prefix'].title()+'/'+id.title()
                full_event['event_path'] = events_dir
                full_event['duration']   = int(full_event['duration'])
                # Add event to global events list
                full_id = events_config['prefix'].lower()+'/'+id.lower()
                events[full_id]=full_event

        return profile, events



    # --------------------------------------------------------------
    # -- Init TimeSheetManager
    # --------------------------------------------------------------
    #
    def __init__(self, profile_path, debug=0):
        '''
        Init TimeSheetManager
        args:
            profile_path : Path to the profile file
            debug : debug level 0:none 1:debug traces (0)
        return:
            nothing
        '''

        self.__debug_level = debug

        print(f'\n=== Fidle/TimeSheetManager - Management of presence sheets')
        print(f'=== Version : {self.__version__}\n')

        # ---- Load profile
        #
        profile, events = self.__read_profile(profile_path)

        # ---- Retrieve infos (sequences key must be titled)
        #
        self.config  = profile
        self.events  = events
        
        print('TimeSheetManager init')
        print(f'    Profile      : {profile_path}')
        print(f'    Events       : {len(self.events)}\n')



    def __open_M(self):
        '''
        Open IMAP session
        '''
        imap_server  = self.config['imap_server']
        imap_login   = self.config['imap_login']
        imap_passwd  = self.config['imap_password']

        M = imaplib.IMAP4_SSL(imap_server)
        M.login(imap_login, imap_passwd)

        self.__M = M


    def __close_M(self):
        '''
        Close IMAP session
        '''
        self.__M.close()
        self.__M.logout()


    def __debug(self,*what):
        '''
        Print debug infos, if debug level is >0..
        args:
            *what: stuffs to print
        '''
        if self.__debug_level <1: return
        for w in what:
            print(w)


    
    def __open_S(self):
        '''
        Open SMTP session
        '''

        smtp_server    = self.config['smtp_server']
        smtp_port      = self.config['smtp_port']
        smtp_login     = self.config['smtp_login']
        smtp_passwd    = self.config['smtp_password']
        smtp_ssl       = self.config['smtp_ssl']

        if smtp_ssl:
            S = smtplib.SMTP_SSL(smtp_server,port=smtp_port)
            S.ehlo()
        else:
            S = smtplib.SMTP(smtp_server,port=smtp_port)
            S.ehlo()
            S.starttls() 

        S.login(smtp_login, smtp_passwd)

        self.__S = S


    def __close_S(self):
        '''
        Close SMTP session
        '''
        self.__S.quit()



    def __check_imap_status(self,status,data):
        '''
        Check imaplib return status. Raise an exception if not ok.
        '''
        if status != 'OK' : raise RuntimeError(data[0])


    def __visa_encode(self, email, event_id):
        '''
        Encode a visa from email and event_id
        args:
            email : email of participant
            event_id : followed event_id
        return:
            base32 visa
        '''
        event_id    = event_id.lower()
        event       = self.events[event_id]
        magic_token = event['magic_token']
        digest_size = event['digest_size']

        secret_text = f'{email.lower()} {magic_token} {event_id}'

        h = hashlib.blake2b(digest_size=digest_size)
        h.update(secret_text.encode('UTF8'))
        visa_b = h.digest()
        visa = base64.b32encode(visa_b).decode('ascii').upper()
        return visa




    def __get_confirmation(self, presence):
        
        module_dir       = pathlib.Path(__file__).parent
        
        event_id  = presence['event_id'].lower()
        event = self.events[event_id]

        mail_template    = event['mail_template']
        mail_from        = event['mail_from']
        mail_contact     = event['mail_contact']
        recovery_url     = event['recovery_url']

        mail_to          = presence['from']
        attestation_visa = presence['attestation_visa']

        # encoded = base64.b64encode(open(f'{module_dir}/img/00-Fidle-logo-01_m.png', "rb").read()).decode('utf-8')
        # logo_ender = '<img src="data:image/png;base64,'+encoded+'"/>'

        direct_url = recovery_url + '?m={mail_id}&s={event_id}&v={attestation_visa}'
        direct_url = direct_url.format( mail_id          = mail_to, 
                                        event_id         = event_id, 
                                        attestation_visa = attestation_visa,
                                        mail_contact     = mail_contact)

        # ---- Load template
        # 
        if mail_template=='default':
            template_path = f'{module_dir}/templates/attestation_mail'
        else:
            template_path = mail_template

        template_txt  = Template( open(template_path+'.txt' ).read() )
        template_html = Template( open(template_path+'.html').read() )

        # ---- Template substitution
        #
        subject = f'Attestation confirmation - {mail_to}' 
        html    = template_html.substitute( recovery_url     = recovery_url,
                                            mail_id          = mail_to,
                                            event_id         = event_id, 
                                            attestation_visa = attestation_visa,
                                            direct_url       = direct_url,
                                            mail_contact     = mail_contact,
                                            fidle_version    = self.__version__)

        plain   = template_txt.substitute(  recovery_url     = recovery_url,
                                            mail_id          = mail_to, 
                                            event_id         = event_id,
                                            attestation_visa = attestation_visa,
                                            direct_url       = direct_url,
                                            mail_contact     = mail_contact,
                                            fidle_version    = self.__version__)
        
        # ---- Create mail
        #
        # Create message container -  MIME is multipart/alternative.
        #
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From']    = mail_from
        msg['To']      = mail_to

        # Two parts : text/plain and text/html.
        #
        part1 = MIMEText(plain, 'plain')
        part2 = MIMEText(html,  'html' )

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message is best and preferred

        msg.attach(part1)
        msg.attach(part2)

        return msg




    def get_presences( self, 
                       event_id  = None, 
                       at        = None, 
                       duration  = 15):
        '''
        Retreive presences mail for a given event
        args:
            event_id : event id to search
            at : valid date start
            duration : valid duration

        return:
            dict of mails
        '''
        self.__debug('== __get_presences() ======')

        print('=== Get presences from mails ===\n')

        # ---- Get event
        #
        if event_id is None: raise('Event id must be defined...') 

        event_id = event_id.lower()
        event = self.events.get(event_id)
        if event is None: raise(f'Event {event_id} cannot be found...') 

        # ---- Retrieve parameters
        #
        imap_inbox   = self.config['imap_inbox']
        mail_to      = event['mail_to']
        event_title  = event['title']
        event_date   = event['date']
        magickey     = event['magickey']
        digest_size  = event['digest_size']
        magic_token  = event['magic_token']

        tz_local     = dateutil.tz.gettz(self.config['tz_local'])

        if magickey is None: raise('Magickey must be defined...') 
        

        # Sequence
        #
        # if sequence_id is None:
        #     sequence_id    = '-'
        #     sequence_title = '-'
        #     sequence_date  = '-'
        # else:
        #     sequence_id    = sequence_id.title()
        #     sequence_title = self.sequences[sequence_id]['title']
        #     sequence_date  = self.sequences[sequence_id]['date']

        # Magic key
        #
        # if magickey is None: 
        #     magickey = self.sequences[sequence_id.title()]['magickey']

        # ---- t1 : from <at>
        #
        if at is None:
            t1 = datetime.datetime.now()
            t1 = t1.astimezone(tz_local)
        else:
            t1 = datetime.datetime.strptime(at, '%d-%m-%Y %H:%M:%S')
            t1 = t1.astimezone(tz_local)

        # ---- t2 : from <t1> + <duration>
        #
        t2 = t1 + datetime.timedelta(minutes=duration)

        # ---- after and before
        #      because duration can be <0
        #
        after  = min(t1,t2)
        before = max(t1,t2)

        # ---- Verbosity
        #
        print('Parameters are :')
        print(f'    Event id     : {event_id.title()}')
        print(f'    Event title  : {event_title}')
        print(f'    Event date   : {event_date}')
        print(f'    Magickey     : {magickey}')
        print(f"    valid after  : {after.strftime('%d-%m-%Y %H:%M:%S')}")
        print(f"    valid before : {before.strftime('%d-%m-%Y %H:%M:%S')}\n")

        # ---- Open IMAP channel
        #
        self.__open_M()
        M= self.__M
        presences = []

        # ---- Build filter
        #
        # filter = f'OR TEXT "{magickey}" SUBJECT "{magickey}" ON "{presence_day}" TO "{mail_to}"'
        # filter = f'OR TEXT "{magickey}" SUBJECT "{magickey}" TO "{mail_to}"'
        filter = f'TO "{mail_to}"'

        # ---- Go to the right box, and search messages
        #
        M.select(imap_inbox)
        # status, data = M.search(None, filter)

        status, uids = M.uid('SEARCH', filter)

        self.__check_imap_status(status,uids)
        self.__debug(f'folder={imap_inbox}',f'filter={filter}',f'status={status}')

        # ---- Split uids and get messages
        #
        mail_uids = []
        for block in uids:
            mail_uids += block.split()
        self.__debug(f'Nb mails={len(mail_uids)}')

        nb_ok = 0
        for uid in mail_uids:

            uid=uid.decode('UTF8')
            # ---- Get Flags
            # status,  flags = M.fetch(id, '(FLAGS)')
            status,  flags = M.uid('FETCH', uid, '(FLAGS)')
            self.__check_imap_status(status,flags)

            flags = flags[0].decode('UTF8')
            self.__debug(f'flags={flags}')

            flag_answered = ( '\Answered' in flags)
            flag_seen     = ( '\Seen'     in flags)

            # ---- Get message
            #
            # status,  data  = M.fetch(id, '(RFC822)')
            status,  data  = M.uid('FETCH',uid, '(RFC822)')
            self.__check_imap_status(status,data)

            # Note : data is a multiparts data structure
            # Dans notre cas, on va considérer que nous n'avons qu'une seule partie.
            # Pour être rigoureux, il faudrait itérer sur les morceaux...
            #
            # for response_part in data:
            #     if not isinstance(response_part, tuple): continue
            #     message     = email.message_from_bytes(response_part[1])

            message     = email.message_from_bytes( data[0][1] )

            msg_to      = email.utils.parseaddr( message.get('to')   )[1]
            msg_from    = email.utils.parseaddr( message.get('from') )[1]
            msg_subject = message.get('subject')
            msg_id      = message.get('Message-ID')

            # ---- Extract content from brut message
            #
            if message.is_multipart():
                msg_content = ''

                for part in message.get_payload():

                    if part.get_content_type() == 'text/plain':
                        msg_content += part.get_payload()
            else:
                msg_content = message.get_payload()

            # ---- Is it a presence message ? (have magickey)
            #
            # msg_magic_content =  ( magickey in msg_content )
            # msg_magic_subject =  ( magickey in msg_subject )
            msg_magic_content =  ( re.search(magickey, msg_content, re.IGNORECASE) is not None )
            msg_magic_subject =  ( re.search(magickey, msg_subject, re.IGNORECASE) is not None )

            # ---- Send date
            #
            msg_send_str = message.get('date')
            msg_send_dt  = email.utils.parsedate_to_datetime(msg_send_str)
            msg_send_dt  = msg_send_dt.astimezone(tz_local)
            msg_send_ok  = (after <= msg_send_dt <= before)
            # print('Send date : ', msg_send_dt.strftime('%A %d %b %Y %H:%M:%S'), msg_send_ok)

            # ---- Received date
            #
            msg_received_str = message.get('received').split(';')[-1]
            msg_received_dt  = email.utils.parsedate_to_datetime(msg_received_str)
            # print('Rec date  : ', msg_received_dt.strftime('%A %d %b %Y %H:%M:%S'))

            # ---- Transit
            #
            dt = msg_received_dt - msg_send_dt
            msg_transit = dt.total_seconds()
            # print(f'Transit   : {msg_transit:.2f}')

            # ---- Age
            #
            now = datetime.datetime.now().astimezone(tz_local)
            dt =  now - msg_send_dt
            msg_age = dt.total_seconds()
            # print(f'Age/send  : {msg_age:.2f} sec.')

            # ---- Check validity
            #      Need valid send date and magic content
            #
            attestation_ok = (msg_magic_content or msg_magic_subject) and msg_send_ok
            if attestation_ok: nb_ok+=1

            # ---- Set visa
            #
            attestation_visa = self.__visa_encode(msg_from, event_id) if attestation_ok else '-'

            # ---- Create presence
            #
            presence = { 'imap_uid'         : uid,
                         'msg_id'           : msg_id,
                         'from'             : msg_from,
                         'to'               : msg_to,
                         'magic_subject'    : msg_magic_subject,
                         'magic_content'    : msg_magic_content,
                         'send_dt'          : msg_send_dt,
                         'send_str'         : msg_send_str,
                         'send_ok'          : msg_send_ok,
                         'received_dt'      : msg_received_dt,
                         'received_str'     : msg_received_str,
                         'transit'          : msg_transit,
                         'age'              : msg_age,
                         'flag_answered'    : flag_answered,
                         'flag_seen'        : flag_seen,
                         'attestation_ok'   : attestation_ok,
                         'attestation_visa' : attestation_visa,
                         'event_id'         : event_id
            }
            presences.append(presence)

        self.__close_M()

        # ---- Verbosity
        #
        print('Presences :')
        print(f'    Found in folder : {len(presences)}')
        print(f'    Attestations ok : {nb_ok}\n')

        return presences



    def send_confirmations(self, presences, event_id, flag_answered=True, archive_answered=True):
        '''
        Sending confirmations for the given presence list.
        Confirmations are sent only if attestation_ok is true.
        args:
            presences     : presences list
            save_copy     : Save a copy of each confirmation email sent (False)
            flag_answered : Set the answered flag of the emails to which a confirmation is sent (False)
        returns:
            nothing
        '''

        # ---- Get event
        #
        if event_id is None: raise('Event id must be defined...') 

        event_id = event_id.lower()
        event = self.events.get(event_id)
        if event is None: raise(f'Event {event_id} cannot be found...') 

        event_subfolder = re.sub('[^A-Za-zÀ-ÿ0-9\-\._\/ ]','',event_id)

        # ---- Retrieve parameters
        #
        imap_inbox    = self.config['imap_inbox']
        
        imap_archbox  = self.config['imap_archbox']
        imap_sentbox  = f'{imap_archbox}/{event_subfolder}/attestations'
        imap_donebox  = f'{imap_archbox}/{event_subfolder}/presences'
        
        smtp_max      = self.config['smtp_max']
        smtp_delay    = self.config['smtp_delay']

        print('=== Send confirmations ===\n')
        print('Parameters are :')
        print(f'    Input box       : {imap_inbox}')
        print(f'    Archive box     : {imap_archbox}')
        print(f'    Flag answered   : {flag_answered}')
        print(f'    Archive answered: {archive_answered}\n')

        print('[x]: Invalid message  [o]: Confirmation sent  [.]:Previously answered\n')

        # ---- Open SMTP session
        #
        self.__open_S()
        S=self.__S

        # ---- Open IMAP session
        #
        self.__open_M()
        M= self.__M

        # ---- Create archive folders
        #
        if archive_answered:
            M.create(imap_sentbox)
            M.create(imap_donebox)

        # ---- Iterate on presences
        #
        nb_sent=0
        for p in presences:
        
            # ---- Attestation not ok : Do nothing 
            #
            if not p.get('attestation_ok',False):
                print('[x]', end='')
                continue
            
            # ---- Attestation ok, but already answered : Do nothing
            #
            if p.get('flag_answered'):
                print('[.]', end='')
                continue

            # ---- Attestation ok : Send answer
            #
            # Prepare message
            message = self.__get_confirmation(p)

            # Send it
            S.send_message(message)
            time.sleep(smtp_delay)
            nb_sent+=1

            # ---- Flag answered ?
            if flag_answered : 
                M.select( imap_inbox    )
                uid=p['imap_uid']
                M.uid( 'STORE', uid, '+FLAGS', '(\\Answered)')
                p['flag_answered']=True
                
            # ---- Archive answered ?
            if archive_answered : 
                # Archive a copy to : imap_sentbox
                M.append( imap_sentbox, 
                          '\Seen', 
                          imaplib.Time2Internaldate(time.time()), 
                          str(message).encode('utf-8') )
                # Move answered mail to : imap_donebox
                M.select( imap_inbox    )
                uid=p['imap_uid']
                M.uid( 'COPY',  uid, imap_donebox)
                M.uid( 'STORE', uid, '+FLAGS', '(\\Deleted)')

            # Trace
            print('[o]', end='')
            
            # Max sent ?
            if nb_sent>= smtp_max: 
                print('[...]', end='')
                break
                
        print('\n')
        self.__close_S()

        print(f'Number of confirmations sent : {nb_sent}\n')

        return



    def show_uids(self):

        imap_inbox     = self.config['imap_inbox']

        self.__open_M()
        M= self.__M

        M.select( imap_inbox)
        uids = M.uid('SEARCH', 'ALL')
        print(uids)



    def unflag(self, presences):
        '''
        Remove anwered and seen flags from given presence emails.
        Only emails with a valid send date are updated.
        args:
            presences : list of presences
        return
            number of changed presence emails
        '''

        print('=== Remove flags ===\n')

        imap_inbox     = self.config['imap_inbox']

        self.__open_M()
        M= self.__M

        M.select( imap_inbox )

        nb_changed=0
        for p in presences:
            if p['send_ok'] and ( p['flag_answered'] or p['flag_seen'] ):
                uid=p['imap_uid']
                M.uid( 'STORE', uid, '-FLAGS', '\\Answered \\seen')
                p['flag_seen']     = False
                p['flag_answered'] = False
                nb_changed+=1

        print(f'Number of unflag emails : {nb_changed}\n')



    def save_presences(self, presences, save_as=None, default='Presences'):
        '''
        Save given presences as a nice csv file
        if save_as is None : do nothing
        is save_as is 'default' : use default base name
        args:
            presences : presences data
            save_as : filename to use, None or 'default'
            default : default base name to use if save_as is 'default'
        return:
            nothing
        '''

        # No need to save
        if save_as is None: return

        # Define filename
        if save_as=='default':
            filename=f'{default}-{Chrono.tag_now()}.csv'
        else:
            filename=save_as

        # Save it
        print('=== Save presences sheet ===\n')
        df = pd.DataFrame.from_dict(presences)
        df.to_csv(filename,sep=';')
        print(f'    Saved as     : {filename}')


        # df = df[ ['from','send_str','send_dt','transit','attestation_ok','sequence_id'] ]
        # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 2000):
        #     display(df)
