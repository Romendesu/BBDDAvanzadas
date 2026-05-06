from flask import Blueprint, request, render_template, abort
from models import OperacionesCurso, OperacionesProfesor
from config import PAGE_SIZE

asignaturas_bp = Blueprint('asignaturas', __name__, url_prefix="/asignaturas")


@asignaturas_bp.route('/')
def home():
    q    = request.args.get('q', '').strip()
    page = max(1, request.args.get('page', 1, type=int))

    all_rows = OperacionesCurso().get_all_courses_with_count()

    if q:
        ql = q.lower()
        all_rows = [r for r in all_rows if ql in r[1].lower() or ql in r[2].lower()]

    filtered    = len(all_rows)
    total       = OperacionesCurso().get_count()
    total_pages = max(1, -(-filtered // PAGE_SIZE))
    page        = min(page, total_pages)

    start = (page - 1) * PAGE_SIZE
    rows  = all_rows[start:start + PAGE_SIZE]

    p_start = max(1, page - 2)
    p_end   = min(total_pages, p_start + 4)
    pages   = list(range(p_start, p_end + 1))

    profesores = OperacionesProfesor().get_all_teachers()

    return render_template(
        "asignaturas/list.html",
        title="Asignaturas",
        rows=rows,
        total=total,
        filtered=filtered,
        q=q,
        page=page,
        total_pages=total_pages,
        pages=pages,
        profesores=profesores,
    )


@asignaturas_bp.route('/<curso_id>')
def detail(curso_id):
    gestor = OperacionesCurso()
    curso  = gestor.get_by_id(curso_id)
    if not curso:
        abort(404)
    alumnos = gestor.get_alumnos_by_curso(curso_id)
    return render_template(
        "asignaturas/detail.html",
        title=curso[1],
        curso=curso,
        alumnos=alumnos,
    )
