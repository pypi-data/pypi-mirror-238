import os
import csv
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time
import logging
import ctypes
from psycopg2 import Error
from python.xPostgreSQL import Config as PostgreSQLConfig
from python.xMySQL import Config as MySQLConfig
from python.xConfigparser import Config as Config
from colorama import init, Fore, Back, Style

class DatabaseConnector:
    def __init__(self, db, host, user, pw, port, schemas):
        self.db = db
        self.host = host
        self.user = user
        self.pw = pw
        self.port = port
        self.schemas = schemas

    def connectPostgreSQL(self):
        try:
            # PostgreSQLConfigクラスを使用してデータベースに接続
            connection = PostgreSQLConfig(self.db, self.host, self.user, self.pw, self.port, self.schemas)
            return connection
        except (Exception, Error) as error:
            # データベースへの接続中にエラーが発生した場合はRuntimeErrorを発生させる
            raise RuntimeError(f"データベースへの接続エラー: {error}")
        
    def connectMySQL(self):
        try:
            # PostgreSQLConfigクラスを使用してデータベースに接続
            connection = MySQLConfig(self.db, self.host, self.user, self.pw)
            return connection
        except (Exception, Error) as error:
            # データベースへの接続中にエラーが発生した場合はRuntimeErrorを発生させる
            raise RuntimeError(f"データベースへの接続エラー: {error}")

class EmailNotifier:
    def __init__(self, smtp_server,smtp_port,sender):
        self.smtp_server=smtp_server
        self.smtp_port=smtp_port
        self.sender = sender

    def get_files_in_folders(folder_paths):
        file_paths = []
        file_names = []
        for folder_path in folder_paths:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_paths.append(os.path.join(root, file))
                    file_names.append(file)
        return file_paths, file_names

    def send_email(self,subject,header,body,footer,recipients,recipients_cc):
        try:
            # Email details
            smtp_server = self.smtp_server
            smtp_port = self.smtp_port
            sender = self.sender

            # Create a MIME text object
            msg = MIMEMultipart()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ';'.join(recipients)
            if recipients_cc!='':
                msg['CC'] = ';'.join(recipients_cc)

            table_html = ''
            if body != '':
                table_html = body
            
            # Create the email body as HTML
            message = header
            message += f'<html><body>{table_html}</body></html>'
            message += footer

            # Attach the email body
            msg.attach(MIMEText(message, 'html'))

            # Connect to the SMTP server
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                try:    
                    server.sendmail(sender, recipients, msg.as_string())
                    return 1
                except Exception as e:
                    print('An error occurred:', str(e))
                    return 0
                finally:
                    # Disconnect from the SMTP server
                    server.quit()
        except Exception as e:
            # Email通知の送信中にエラーが発生した場合はRuntimeErrorを発生させる
            raise RuntimeError(f"Email通知の送信エラー: {e}")


class Template:
    def __init__(self,config_file):
        # Configクラスを使用して設定ファイルから設定を読み込む
        self.db = None
        self.host = None
        self.user = None
        self.pw = None
        self.port = None
        self.schemas = None
        self.log = None
        self.console_title = None
        self.smtp_server = None
        self.smtp_port = None
        self.sender = None

        self.configuration = Config(config_file)
        try:
            self.db = self.configuration.get('DB', 'db')
            self.host = self.configuration.get('DB', 'host')
            self.user = self.configuration.get('DB', 'user')
            self.pw = self.configuration.get('DB', 'pw')
            self.port = self.configuration.get('DB', 'port')
            self.schemas = self.configuration.get('DB', 'schemas')
        except Exception as e:
            print(f"Exception error: {str(e)}")

        try:
            self.smtp_server = self.configuration.get('EMAIL', 'smtp_server')
            self.smtp_port = self.configuration.get('EMAIL', 'smtp_port')
            self.sender = self.configuration.get('EMAIL', 'sender')
        except Exception as e:
            print(f"Exception error: {str(e)}")
            
        try:
            self.log = self.configuration.get('PARAM', 'log')
            self.console_title = self.configuration.get('PARAM', 'console_title')
        except Exception as e:
            print(f"Exception error: {str(e)}")
        

        # DatabaseConnectorおよびEmailNotifierの初期化
        self.database_connector = DatabaseConnector(
            self.db,
            self.host,
            self.user,
            self.pw,
            self.port,
            self.schemas
        )
        self.email_notifier = EmailNotifier(
            self.smtp_server,
            self.smtp_port,
            self.sender
        )

        # その他の変数の初期化...
        self.console_title = self.console_title

        console_handle = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.kernel32.SetConsoleTitleW(self.console_title)

        init(autoreset=True)                                            # autoreset=Trueを設定して、Coloramaのテキストリセットを有効にします。
        logging.basicConfig(filename=self.log, level=logging.INFO, encoding="utf-8")

    def config(self,section,value):
        return self.configuration.get(section, value)

    def export_to_csv(self,file_path,message):
        if self.boxno_entry.get():
            with open(file_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                
                # Write the header row
                header = [self.data_table.heading(column)["text"] for column in self.data_table["columns"]]
                writer.writerow(header)

                # Write the data rows
                for row_id in self.data_table.get_children():
                    row = [self.data_table.item(row_id, "values")[i] for i in range(len(header))]
                    writer.writerow(row)

            messagebox.showinfo("INFO", message)

    def db_fetchall(self,query):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectPostgreSQL()
            # クエリの実行
            return db_connection.fetchall(query)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("ERROR2:", error)
            self.handle_error(error)

    def db_commit(self,query):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectPostgreSQL()
            # クエリの実行
            return db_connection.commit(query)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("ERROR2:", error)
            self.handle_error(error)

    def db_commit_values(self,query,values):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectPostgreSQL()
            # クエリの実行
            return db_connection.commit_values(query,values)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("ERROR2:", error)
            self.handle_error(error)

    def db_commit_many(self, query, values):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectPostgreSQL()
            # クエリの実行
            return db_connection.commit_many(query, values)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("ERROR2:", error)
            self.handle_error(error)

    def mySQL_fetchall(self,query):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL()
            # クエリの実行
            return db_connection.fetchall(query)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("ERROR2:", error)
            self.handle_error(error)

    def mySQL_commit(self,query):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL()
            # クエリの実行
            return db_connection.commit(query)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("ERROR2:", error)
            self.handle_error(error)

    def mySQL_commit_values(self,query,values):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL()
            # クエリの実行
            return db_connection.commit_values(query,values)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("ERROR2:", error)
            self.handle_error(error)

    def mySQL_commit_many(self, query, values):
        try:
            # データベースへの接続
            db_connection = self.database_connector.connectMySQL()
            # クエリの実行
            return db_connection.commit_many(query, values)

        except Exception as error:
            # エラーが発生した場合はエラーハンドリングを実行
            print("ERROR2:", error)
            self.handle_error(error)

    def run_interval(self):
        while True:
            print("システムを起動しています")
            if not self.in_process_flag:
                self.in_process_flag = True
                try:
                    self.main()
                finally:
                    self.in_process_flag = False
            interval = int(self.interval)
            time.sleep(interval)
 
    def handle_error(self, error):
        print("Error2:", error)
        logging.basicConfig(filename="error.log", level=logging.ERROR)
        # 現在の日時を取得
        now = datetime.datetime.now()
        # エラーログを記録
        logging.error(now.strftime("%Y-%m-%d %H:%M:%S") + " " + str(error))

    def print(self, OKNG,info):
        now = datetime.datetime.now()
        if OKNG == "OK":
            # OKの場合のメッセージ
            message = f" {Fore.WHITE}{Back.YELLOW}{Style.BRIGHT}{now.strftime('%Y-%m-%d %H:%M:%S')}{Back.BLACK} {info} {Style.NORMAL}"
        else:
            # NGの場合のメッセージ
            message = f" {now.strftime('%Y-%m-%d %H:%M:%S')}{Fore.WHITE}{Back.RED}{Style.BRIGHT} {info} {Style.NORMAL}"

        print(message)

    def logging_date(self,info):
        now = datetime.datetime.now()
        log_message = f" {now.strftime('%Y-%m-%d %H:%M:%S')} {info}"
        logging.info(log_message)

    def logging(self,info):
        log_message = f" {info}"
        logging.info(log_message)

    def send_email(self, message):
        # Extract message components from the dictionary
        message_body = message.get("message_body")
        recipient = message.get("recipient")
        recipient_cc = message.get("recipient_cc")
        subject = message.get("subject")
        header = message.get("header")
        header2 = message.get("header2")
        footer = message.get("footer")
        footer2 = message.get("footer2")

        recipient = recipient.split(';')
        recipient_cc = recipient_cc.split(';')
        message_header = f"{header}<br><br>"
        message_header += f"<font style='color:blue;font-weight:bold;font-size:18px'>{header2}</font><br><br>"
        message_footer = f"<br><br>{footer}<br><br>{footer2}"
        # Email通知の送信
        self.email_notifier.send_email(subject, message_header,message_body, message_footer, recipient, recipient_cc)



