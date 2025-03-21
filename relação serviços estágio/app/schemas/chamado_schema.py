from marshmallow import Schema, fields

class ChamadoSchema(Schema):
    id = fields.Int(dump_only=True)
    data = fields.Date(required=True)
    horario = fields.Time(required=True)
    estagiario = fields.Str(required=True)
    unidade = fields.Str(required=True)
    sala = fields.Str(required=True)
    professor = fields.Str(required=True)
    motivo = fields.Str(required=True)
    descricao = fields.Str(required=True)