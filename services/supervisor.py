from sqlalchemy.orm import Session

from models.supervisors import Supervisors


def get_supervisor_from_id(
    supervisor_id: str, db: Session
) -> Supervisors | None:
    return db.query(Supervisors).filter_by(id=supervisor_id).first()
