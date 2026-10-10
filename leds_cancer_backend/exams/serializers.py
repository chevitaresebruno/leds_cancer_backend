from rest_framework import serializers

from .models import Exam

DATE_FORMAT = "%d/%m/%Y"
DATETIME_FORMAT = "%d/%m/%Y %H:%M"


class ExamSummaryForPatientSerializer(serializers.ModelSerializer):
    """Serializer compacto de exame aninhado no detalhe do paciente.

    Corresponde à interface ``PatientExam`` esperada pelo frontend.
    Importado de forma lazy pelo app ``patients`` para evitar circulares.
    """

    date = serializers.DateField(source="exam_date", format=DATE_FORMAT)
    type = serializers.SerializerMethodField()
    radiologist = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ("id", "date", "type", "status", "radiologist")

    def get_type(self, obj: Exam) -> str:
        """Retorna o label legível da técnica do exame."""
        return obj.exam_type

    def get_radiologist(self, obj: Exam) -> str:
        """Retorna o nome do radiologista ou texto padrão."""
        return obj.radiologist_name


class RecentExamSerializer(serializers.ModelSerializer):
    """Serializer para o feed de exames recentes do dashboard.

    Corresponde à interface ``RecentExam`` esperada pelo frontend.
    Usado em ``GET /api/exams/recent/``.
    """

    patient_name = serializers.CharField(source="patient.name")
    datetime = serializers.SerializerMethodField()
    exam_type = serializers.SerializerMethodField()
    error = serializers.CharField(read_only=True, allow_null=True)

    class Meta:
        model = Exam
        fields = ("id", "patient_name", "datetime", "exam_type", "status", "error")

    def get_datetime(self, obj: Exam) -> str:
        """Retorna data/hora de criação no formato ``dd/MM/yyyy HH:MM``."""
        return obj.created_at.strftime(DATETIME_FORMAT)

    def get_exam_type(self, obj: Exam) -> str:
        """Retorna o label legível da técnica do exame."""
        return obj.exam_type


class ExamListSerializer(serializers.ModelSerializer):
    """Serializer completo para o histórico e detalhe individual de exames.

    Usado nos endpoints ``GET /api/exams/`` e ``GET /api/exams/{id}/``.
    Inclui dados desnormalizados do paciente e do radiologista para
    evitar chamadas extras no frontend.
    """

    patient_id = serializers.IntegerField(source="patient.id")
    patient_name = serializers.CharField(source="patient.name")
    datetime = serializers.SerializerMethodField()
    exam_type = serializers.SerializerMethodField()
    radiologist = serializers.SerializerMethodField()
    breast_side = serializers.CharField()
    requesting_physician = serializers.CharField()
    clinical_history = serializers.CharField()
    error = serializers.CharField(read_only=True, allow_null=True)

    class Meta:
        model = Exam
        fields = (
            "id",
            "patient_id",
            "patient_name",
            "datetime",
            "exam_type",
            "status",
            "radiologist",
            "breast_side",
            "requesting_physician",
            "clinical_history",
            "error",
        )

    def get_datetime(self, obj: Exam) -> str:
        """Retorna data/hora de criação no formato ``dd/MM/yyyy HH:MM``."""
        return obj.created_at.strftime(DATETIME_FORMAT)

    def get_exam_type(self, obj: Exam) -> str:
        """Retorna o label legível da técnica do exame."""
        return obj.exam_type

    def get_radiologist(self, obj: Exam) -> str:
        """Retorna o nome do radiologista ou texto padrão."""
        return obj.radiologist_name


class ExamWriteSerializer(serializers.ModelSerializer):
    """Serializer para criação e atualização de exames.

    Aceita upload de imagem via multipart/form-data.
    Campos ``image_file``, ``status``, ``radiologist``,
    ``clinical_history`` e ``requesting_physician`` são opcionais.
    """

    exam_date = serializers.DateField(
        format=DATE_FORMAT,
        input_formats=[DATE_FORMAT, "%Y-%m-%d"],
    )

    llm_version = serializers.CharField(
        write_only=True, required=False, allow_blank=True, allow_null=True
    )
    pdai_version = serializers.CharField(
        write_only=True, required=False, allow_blank=True, allow_null=True
    )

    class Meta:
        model = Exam
        fields = (
            "patient",
            "exam_date",
            "technique",
            "breast_side",
            "clinical_history",
            "requesting_physician",
            "image_file",
            "status",
            "radiologist",
            "llm_version",
            "pdai_version",
        )
        extra_kwargs = {  # noqa: RUF012
            "image_file": {"required": False},
            "status": {"required": False},
            "radiologist": {"required": False},
            "clinical_history": {"required": False},
            "requesting_physician": {"required": False},
        }


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer dos contadores retornados por ``GET /api/dashboard/stats/``."""

    today_patients = serializers.IntegerField()
    pending_exams = serializers.IntegerField()
    monthly_diagnostics = serializers.IntegerField()
    concluded_today = serializers.IntegerField()


class ExamImageTokenSerializer(serializers.Serializer):
    """Serializer da resposta de ``POST /api/exams/{id}/image-token/``.

    Os dois campos devem ser repassados como query params ao chamar
    ``GET /api/exams/{id}/image/?token=<token>&expires=<expires_at>``.
    """

    token = serializers.CharField(
        help_text="HMAC-SHA256 hex — envie como query param ?token= na rota de download."
    )
    expires_at = serializers.IntegerField(
        help_text="Unix timestamp de expiração — envie como query param ?expires= na rota de download."
    )
