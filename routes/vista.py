from flask import Blueprint, request, render_template
from models import OperacionesVista
from config import PAGE_SIZE

vista_bp = Blueprint('vista', __name__, url_prefix="/vista")


@vista_bp.route('/')
def home():
    q    = request.args.get('q', '').strip()
    page = max(1, request.args.get('page', 1, type=int))

    all_rows = OperacionesVista().get_all()

    if q:
        ql = q.lower()
        all_rows = [r for r in all_rows
                    if ql in r[0].lower() or ql in r[1].lower() or ql in r[2].lower()]

    filtered    = len(all_rows)
    total       = OperacionesVista().get_count()
    total_pages = max(1, -(-filtered // PAGE_SIZE))
    page        = min(page, total_pages)

    start = (page - 1) * PAGE_SIZE
    rows  = all_rows[start:start + PAGE_SIZE]

    p_start = max(1, page - 2)
    p_end   = min(total_pages, p_start + 4)
    pages   = list(range(p_start, p_end + 1))

    return render_template(
        "vista/list.html",
        title="Vista: Matrículas",
        rows=rows,
        total=total,
        filtered=filtered,
        q=q,
        page=page,
        total_pages=total_pages,
        pages=pages,
    )
