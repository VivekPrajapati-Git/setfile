from pathlib import Path
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_dir = Path(__file__).resolve().parent.parent.parent.parent/"logs"
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / "setfile.log"
        self.error_log = self.log_dir / "error.log"
        self.moves_log = self.log_dir / "moves.log"

    def _write(self,level,message):
        timestamp = datetime.now()

        if level == ' ERROR ':
            log_path = self.error_log
        elif level == " MOVE ":
            log_path = self.moves_log
        else:
            log_path = self.log_file

        with open(log_path , "a") as f:
            if level == ' MOVE ':
                run_id = message[0]
                file_path = message[1]
                destination = message[2]
                result = f"{timestamp} | {run_id} | {level} | {file_path} -> {destination}"
            else:
                result = f"{timestamp} | {level} : {message}"
            f.write(result + "\n")

    def info(self,message):
        self._write(" INFO ", message)

    def error(self,message):
        self._write(" ERROR ", message)

    def warning(self,message):
        self._write(" WARNING ", message)

    def moves(self,run_id , file_path , destination):
        message = [run_id,file_path,destination]
        self._write(" MOVE ", message)

logger = Logger()