from flask import Blueprint, request, render_template, jsonify, session, redirect, url_for
from models import OperacionesAuditoria
from config import PAGE_SIZE

auditoria_bp = Blueprint('auditoria', __name__, url_prefix="/auditoria")


def _require_admin():
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.login'))
    if user.get('rol') != 'admin':
        return None, True
    return user, False


@auditoria_bp.route('/')
def home():
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.login'))

    q    = request.args.get('q', '').strip()
    filtro_entidad = request.args.get('entidad', '').strip()
    filtro_accion  = request.args.get('accion', '').strip()
    page = max(1, request.args.get('page', 1, type=int))

    all_rows = OperacionesAuditoria().get_all()
    total    = OperacionesAuditoria().get_count()

    if q:
        ql = q.lower()
        all_rows = [r for r in all_rows if ql in (r[1] or '').lower() or ql in (r[4] or '').lower() or ql in (r[5] or '').lower()]
    if filtro_entidad:
        all_rows = [r for r in all_rows if r[3] == filtro_entidad]
    if filtro_accion:
        all_rows = [r for r in all_rows if r[2] == filtro_accion]

    filtered    = len(all_rows)
    total_pages = max(1, -(-filtered // PAGE_SIZE))
    page        = min(page, total_pages)

    start = (page - 1) * PAGE_SIZE
    rows  = all_rows[start:start + PAGE_SIZE]

    p_start = max(1, page - 2)
    p_end   = min(total_pages, p_start + 4)
    pages   = list(range(p_start, p_end + 1))

    is_admin = user.get('rol') == 'admin'

    return render_template(
        "auditoria/list.html",
        title="Auditoría",
        rows=rows,
        total=total,
        filtered=filtered,
        q=q,
        filtro_entidad=filtro_entidad,
        filtro_accion=filtro_accion,
        page=page,
        total_pages=total_pages,
        pages=pages,
        is_admin=is_admin,
    )


@auditoria_bp.route('/delete/<int:audit_id>', methods=['POST'])
def delete(audit_id):
    user = session.get('user')
    if not user or user.get('rol') != 'admin':
        return jsonify(ok=False, error='Acceso denegado. Solo administradores.')
    try:
        OperacionesAuditoria().delete_by_id(audit_id)
        return jsonify(ok=True, message='Registro eliminado correctamente.')
    except Exception as e:
        return jsonify(ok=False, error=str(e))


@auditoria_bp.route('/delete-all', methods=['POST'])
def delete_all():
    user = session.get('user')
    if not user or user.get('rol') != 'admin':
        return jsonify(ok=False, error='Acceso denegado. Solo administradores.')
    try:
        OperacionesAuditoria().delete_all()
        return jsonify(ok=True, message='Historial de auditoría limpiado correctamente.')
    except Exception as e:
        return jsonify(ok=False, error=str(e))
