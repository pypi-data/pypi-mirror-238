from .novadata_model import NovadataModel


class AbstractNovadataModel(NovadataModel):
    class Meta:
        """Sub classe para definir meta atributos da classe principal."""

        abstract = True
