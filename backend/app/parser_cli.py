# backend/app/parser_cli.py
import typer
import json
from app.log_parser import parse_log_file, parse_log_file_from_data, events_to_summary

app = typer.Typer(help="Parser CLI for 6G-Valid8")

@app.command()
def parse(path: str):
    events = parse_log_file(path)
    out = {"events": events, "summary": events_to_summary(events)}
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    app()
