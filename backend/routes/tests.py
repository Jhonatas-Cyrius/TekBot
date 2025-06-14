# backend/routes/tests.py
import json
from fastapi import APIRouter, Response, Query
from subprocess import run, PIPE

router = APIRouter(tags=["Tests"])

@router.get("/")
def list_tests(
    response: Response,
    _start: int = Query(0, alias="_start"),
    _end:   int = Query(10, alias="_end"),
):
    """
    Executa o pytest com --json-report e retorna um slice dos resultados,
    além de expor o Content-Range para o React-Admin.
    """
    # 1) Executa os testes e gera .report.json
    run(
        ["pytest", "--json-report", "--maxfail=1", "--disable-warnings"],
        check=False
    )

    # 2) Abre o relatório JSON
    try:
        with open(".report.json", "r") as f:
            report = json.load(f)
    except FileNotFoundError:
        # Sem report, devolve lista vazia
        response.headers["Content-Range"] = "0-0/0"
        return []

    # 3) Constrói a lista de dicionários
    all_tests = []
    for t in report.get("tests", []):
        all_tests.append({
            "id":   t["nodeid"],
            "name": t["nodeid"],
            "status": t["outcome"],
            "date":   report.get("created")
        })

    # 4) Paginação manual via slicing
    total = len(all_tests)
    slice_ = all_tests[_start:_end]  # pega do _start (inclusive) até _end (exclusive)

    # 5) Calcula o índice final (end index = start + len(slice) - 1)
    end = _start + len(slice_) - 1 if total else 0

    # 6) Define o Content-Range header
    response.headers["Content-Range"] = f"{_start}-{end}/{total}"

    # 7) Retorna apenas o slice
    return slice_
