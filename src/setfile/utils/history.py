from pathlib import Path

def log_reader():
    path = Path(__file__).resolve().parent.parent.parent.parent/"logs/moves.log"
    result = {}
    
    with open(path, 'r') as content:
        for line in content:
            parts = line.strip().split('|')

            run_id = parts[1]

            moves = parts[3]
            src , des = moves.split('->')

            if run_id not in result:
                result[run_id] = []

            result[run_id].append({
                "src" : src,
                "des" : des
            })
    return result.popitem()