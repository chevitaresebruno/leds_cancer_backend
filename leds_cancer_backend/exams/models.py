from django.conf import settings
from django.db import models
from patients.models import Patient
from scripts import IAIService, LaudoStatus, LaudoPayload


class ExamStatus(models.TextChoices):
    """Status possíveis de um exame de mamografia."""

    EM_ANALISE = "em_analise", "Em análise"  # em análise pelo serviço de IA
    PENDENTE = "pendente", "Pendente"  # aguardando ação do médico após análise da IA
    CONCLUIDO = "concluido", "Concluído"  # já analisado pelo médico
    CANCELADO = "cancelado", "Cancelado"  # status de erro vindo do serviço de IA
    NOT_SENT = (
        "não enviado",
        "Não Enviado",
    )  # o exame foi criado com sucesso, mas houve um erro en enviá-lo para a API

    @staticmethod
    def from_laudo_status(laudo_status: LaudoStatus) -> "ExamStatus":
        match laudo_status:
            case LaudoStatus.IN_PROCESSING:
                return ExamStatus.EM_ANALISE
            case LaudoStatus.FINISHED:
                return ExamStatus.PENDENTE
            case LaudoStatus.ERROR:
                return ExamStatus.CANCELADO
            case _:
                raise Exception(f"status {laudo_status} nao mapeado")


class ExamTechnique(models.TextChoices):
    """Técnicas de mamografia suportadas pelo sistema."""

    DIGITAL = "digital", "Mamografia Digital"
    TOMOSSINTESE = "3d_tomossintese", "Mamografia 3D (Tomossíntese)"
    CONTRASTE = "contraste", "Mamografia com Contraste"


class BreastSide(models.TextChoices):
    """Lado da mama examinada."""

    ESQUERDA = "esquerda", "Esquerda"
    DIREITA = "direita", "Direita"
    BILATERAL = "bilateral", "Bilateral"


class Exam(models.Model):
    """Representa um exame de mamografia vinculado a um paciente.

    A imagem do exame é armazenada no servidor via upload multipart
    e salva em ``media/exams/images/<ano>/<mês>/``. O acesso externo
    à imagem é controlado por token HMAC (ver ``exams.tokens``).

    Attributes:
        patient: Paciente ao qual o exame pertence (cascade delete).
        exam_date: Data de realização do exame.
        technique: Técnica utilizada (ver ``ExamTechnique``).
        breast_side: Lado examinado (ver ``BreastSide``).
        clinical_history: Histórico clínico e observações (opcional).
        requesting_physician: Nome do médico solicitante (opcional).
        image_file: Arquivo de imagem enviado via upload (opcional).
        status: Status atual do exame (ver ``ExamStatus``).
        radiologist: Profissional que realizou a análise (opcional,
            ``SET_NULL`` ao ser removido).
        created_at: Data/hora de criação (automático).
        updated_at: Data/hora da última atualização (automático).
    """

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="exams",
        verbose_name="Paciente",
    )
    exam_date = models.DateField(verbose_name="Data do exame")
    technique = models.CharField(
        max_length=20,
        choices=ExamTechnique.choices,
        default=ExamTechnique.DIGITAL,
        verbose_name="Técnica",
    )
    breast_side = models.CharField(
        max_length=10,
        choices=BreastSide.choices,
        verbose_name="Lado",
    )
    clinical_history = models.TextField(
        blank=True, default="", verbose_name="Histórico clínico"
    )
    requesting_physician = models.CharField(
        max_length=200,
        blank=True,
        default="",
        verbose_name="Médico solicitante",
    )
    image_file = models.ImageField(
        upload_to="exams/images/%Y/%m/",
        null=True,
        blank=True,
        verbose_name="Imagem",
    )
    status = models.CharField(
        max_length=15,
        choices=ExamStatus.choices,
        default=ExamStatus.NOT_SENT,
        verbose_name="Status",
    )
    radiologist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analyzed_exams",
        verbose_name="Radiologista",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    report_id = models.CharField(
        max_length=255, verbose_name="Report ID", blank=True, null=True
    )

    class Meta:
        verbose_name = "Exame"
        verbose_name_plural = "Exames"
        db_table = "exams_exam"
        ordering = ["-exam_date", "-created_at"]

        constraints = (
            models.CheckConstraint(
                condition=models.Q(report_id__isnull=False)
                | models.Q(status=ExamStatus.NOT_SENT),
                name="exam_report_required_unless_not_sent",
            ),
        )

    @property
    def exam_type(self) -> str:
        """Retorna o label legível da técnica (ex: "Mamografia Digital")."""
        return self.get_technique_display()  # type: ignore[return-value]

    @property
    def radiologist_name(self) -> str:
        """Retorna o nome do radiologista ou ``"Aguardando atribuição"``."""
        if self.radiologist:
            return self.radiologist.get_full_name() or self.radiologist.username
        return "Aguardando atribuição"

    def __send(self, service: IAIService):
        payload = LaudoPayload(self.pk)
        response = service.new_report(payload)
        self.report_id = response.laudo_id
        self.status = ExamStatus.EM_ANALISE

    def update_in_memory_status(self, service: IAIService) -> None | str:
        if self.status == ExamStatus.CONCLUIDO:
            return None
        try:
            if self.status == ExamStatus.NOT_SENT:
                self.__send(service)
            else:
                service_response = service.get_status(self.report_id)
                self.status = ExamStatus.from_laudo_status(service_response.status)
                return service_response.err
        except Exception as e:
            print(e)
            return str(e)

    def update_in_db_status(self, service: IAIService) -> None | str:
        resp = self.update_in_memory_status(service)
        if resp is None:
            self.save()

        return resp

    def __str__(self) -> str:
        return f"{self.patient.name} — {self.exam_type} ({self.exam_date})"
