from datetime import datetime
from app import db

class Chamado(db.Model):
    __tablename__ = 'chamados'
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.Time, nullable=False)
    estagiario = db.Column(db.String(100), nullable=False)
    unidade = db.Column(db.String(50), nullable=False)
    sala = db.Column(db.String(50), nullable=False)
    professor = db.Column(db.String(100), nullable=False)
    motivo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
