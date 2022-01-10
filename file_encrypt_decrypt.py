import time , os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path 
from logging.handlers import RotatingFileHandler
from cryptography.fernet import Fernet

class Watch:
  
    def __init__(self):

        self.observer = Observer()

        self.event_handler = Handler()

        self.base_folder = f'{Path.home()}\Desktop\Dima Privacy Protection'

        self.encrypt_dir = f'{self.base_folder}\Dima_Encrypt'

        self.decrypt_dir = f'{self.base_folder}\Dima_Decrypt'

        Path(self.encrypt_dir).mkdir(parents=True, exist_ok=True)

        Path(self.decrypt_dir).mkdir(parents=True, exist_ok=True)

        self.observers = []

        self.log_file = f'{self.base_folder}\Dima.log.log'

        logging.basicConfig(
            handlers=[RotatingFileHandler(self.log_file, maxBytes=10000000, backupCount=10)],
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)s %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S')
  
    def run(self):

        try:
            self.observer.schedule(self.event_handler, self.base_folder , recursive = True)

            self.observers.append(self.observer)

            self.observer.start()

        except Exception as ex:
            logging.info(f"Error in starting observer -- {ex}")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            try:
                for o in self.observers:
                    o.unschedule_all()
                    o.stop()
            except Exception as ex:
                logging.info(f" Exception in unschedule_all -- {ex}")

        try:
            for o in self.observers:
                o.join()
        except Exception as ex:
            logging.info(f"Exception in observers thread join  -- {ex}")
  
class Handler(FileSystemEventHandler):
  
    def __init__(self):

        self.encrypt_dir = f'{Path.home()}\Desktop\Dima Privacy Protection\Dima_Encrypt'
        self.decrypt_dir = f'{Path.home()}\Desktop\Dima Privacy Protection\Dima_Decrypt'

        self.key_ = b'EAvkyCq09USeJ1TUXU1qelcScnKwKJKK9EQn59BuMsM='        

        self.fernet_obj = Fernet(self.key_)

    def file_encrypt(self ,original_file_name , encrypt_file_name):

        result = 'complete'

        try:
            while True:
                time.sleep(1)
                if os.path.exists(original_file_name):
                    try:
                        with open(original_file_name, 'rb') as file:
                            binary_data = file.read()
                        break
                    except Exception as ex:
                        result = ''
                        logging.info(f"Error in reading file ( {original_file_name} ) in encryption folder  --- >>> {ex}")
                        break
                else:
                    continue

            encrypted = self.fernet_obj.encrypt(binary_data)

            with open(encrypt_file_name, 'wb') as file:
                file.write(encrypted)

            if result == 'complete':
                return 'True'
            else:return 'False'

        except Exception as ex:
            logging.info(f"Error in file encrypt function --- >>> {ex}")
            return 'False'

    def file_decrypt(self, encrypted_file_name , decrypt_file_name):

        result = 'complete'

        try:
            while True:
                time.sleep(1)
                if os.path.exists(encrypted_file_name):
                    try:
                        with open(encrypted_file_name, 'rb') as file:
                            encrypted_data = file.read()
                        break
                    except Exception as ex:
                        result = ''
                        logging.info(f"Error in reading file ( {encrypted_file_name} ) in decryption folder  --- >>> {ex}")
                        break
                else:
                    continue

            decrypted = self.fernet_obj.decrypt(encrypted_data)

            with open(decrypt_file_name, 'wb') as file:
                file.write(decrypted)

            if result == 'complete':
                return 'True'
            else:return 'False'

        except Exception as ex:
            logging.info(f"Error in file decrypt function --- >>> {ex}")
            return 'False'
    
    def on_created(self, event):

        if event.is_directory:
            return None 

        elif os.path.isfile(event.src_path): 

            file_src_dir = os.path.dirname(event.src_path)

            if str(self.encrypt_dir) in str(file_src_dir) :

                if Path(event.src_path).suffix != '.aes' :
                    try:
                        encrypt_file_name  = f"{event.src_path}.aes"

                        original_file_name  = f'{event.src_path}'

                        file_encrypt = self.file_encrypt( original_file_name , encrypt_file_name ) 

                        if file_encrypt == 'True' and os.path.exists(encrypt_file_name):
                            os.remove(original_file_name)

                    except Exception as ex:
                        logging.info(f"Encrypt file exception  --- >>> {ex}")
                else:
                    pass
            else:

                if str(self.decrypt_dir) in str(file_src_dir) :

                    if Path(event.src_path).suffix == '.aes':
                        try:
                            decrypt_file_name = event.src_path.rsplit(".aes", 1)[0]

                            print(decrypt_file_name)

                            encrypted_file_name  = f'{event.src_path}'

                            file_decrypt = self.file_decrypt(encrypted_file_name , decrypt_file_name) 

                            if file_decrypt == 'True' and os.path.exists(decrypt_file_name):
                                os.remove(encrypted_file_name)

                        except Exception as ex:
                            logging.info(f"Decrypt file exception . The given file is not encrypted by DimaAV  --- >>> {ex}") 
                    else:
                        pass  
                else:
                    print(')))))))))))))))))))')
        else: 
            logging.info(f" Invalid file type  --- >>> {event.src_path} !!!") 

    # def on_deleted(self, event):

    #     logging.info(f" File deleted  --  {event.src_path}  !!!")
        
    # def on_modified(self, event):

    #     logging.info(f"The File  {event.src_path} has been modified")
        
    # def on_moved(self, event):

    #     logging.info(f" File Moved From {event.src_path} to {event.dest_path}")
        
              
if __name__ == '__main__':

    watch = Watch()
    watch.run()