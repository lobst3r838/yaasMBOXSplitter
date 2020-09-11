import mailbox
from dateutil.parser import parse
import dateutil.relativedelta
from datetime import datetime
from time import sleep
import sys
import os


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('''
        Mmm... no!

        USO
        split_mbox archivio.mbox numero_di_mesi_che_si_vogliono_estrarre

        ESEMPIO:
        split_mbox mio_archivio.mbox 12

        Questo comando andrà ad estrarre gli ultimi 12 mesi dall'archivio e ne creerà uno nuovo
        ''')
        print(sys.argv)
    else:
        if not sys.argv[2].isnumeric():
            print('\nERRORE: il numero dei mesi deve essere numerico!')
            print("...se to pèder al vliva fer un ignurant l'è sté brev daboun...")
            sys.exit(0)
        if not os.path.isfile(sys.argv[1]):
            print('\nERRORE: file non trovato.')
            print("...i miràcol i fa i sant e'l ragàzi sèinza i mutànt...")
            sys.exit(0)
        archive_name = sys.argv[1]
        months_to_extract = int(sys.argv[2])

        mbox = mailbox.mbox(archive_name)
        print('\nInizio scansione mailbox... la procedura potrebbe impiegare molto tempo in base alla dimensione del file\n')
        ids = {}
        errors = 0
        for key, message in mbox.iteritems():
            if message['X-Gmail-Labels'] != 'Chat':
                # aggiungo al dizionario 
                # chiave = id del messaggio mbox
                # valore = timestamp del messaggio
                # ids[key] = parse(message['Date']).timestamp()
                try:
                    ids[key] = parse(message['Date'])
                except:
                    errors += 1

            
        # ora devo ordinare tutti gli elementi del dizionario per valore
        sorted_ids = sorted(ids.items(), key=lambda x: x[1], reverse=False)
        first_mail_key = sorted_ids[0][0]
        last_mail_key = sorted_ids[len(sorted_ids)-1][0]

        
        first_message = mbox.get(first_mail_key)
        
        last_message = mbox.get(last_mail_key)
        

        print(f'Inizio divisione mailbox. Mesi selezionati: {months_to_extract}.')
        print('La procedura potrebbe impiegare molto tempo in base al numero di elementi da processare.\n')

        sleep(2)

        last_mail = parse(last_message['Date'])
        date_limit = last_mail - dateutil.relativedelta.relativedelta(months=months_to_extract)

        new_file_name = os.path.splitext(archive_name)[0] + '_SPLITTED' + os.path.splitext(archive_name)[1]
        new_mbox = mailbox.mbox(new_file_name)
        wrote_messages = 0
        for key, ts_date in sorted_ids:
            if ts_date > date_limit:
                m = mbox.get(key)
                print(f'ID: {key}.\nOggetto: {m["Subject"]}\nData: {parse(m["Date"]).date()}\nFrom: {m["From"]}\nTo: {m["To"]}\n--------------------------------------------------\n\n')
                new_mbox.add(m)
                new_mbox.flush()
                wrote_messages += 1
        new_mbox.close()
        mbox.close()

        print('Tot messaggi file origine       :', mbox.__len__())
        print('Errori di lettura               :', str(errors))
        print('Data primo messaggio            :', str(first_message["Date"]))
        print('Data SPLIT                      :', date_limit)
        print('Data ultimo messaggio           :', str(last_message["Date"]))
        print('Messaggi scritti sul nuovo file :', str(wrote_messages))
        print('File creato                     :', new_file_name)
