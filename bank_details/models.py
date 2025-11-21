from __future__ import annotations

import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

# Credit Card Checker

def luhn_check(number: str) -> bool:
    """Luhn mod-10 for card numbers."""
    digits = [int(d) for d in number]
    checksum = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0

def clabe_checksum_ok(clabe: str) -> bool:
    """
    Verifica CLABE de 18 dígitos usando ponderaciones 3,7,1 sobre los primeros 17.
    Dígito verificador = (10 - (suma % 10)) % 10 debe coincidir con el 18°.
    """
    if not re.fullmatch(r"\d{18}", clabe):
        return False
    weights = [3, 7, 1]
    total = 0
    for i in range(17):
        total += (int(clabe[i]) * weights[i % 3]) % 10
    check = (10 - (total % 10)) % 10
    return check == int(clabe[17])


def detect_card_brand(number: str) -> str:
    """
    Detecta marca básica sin APIs:
      - VISA: empieza con 4 (16 dígitos en este MVP)
      - MasterCard: 51–55 o 2221–2720
      - Si no coincide: OTHER
    """
    if len(number) != 16:
        return "Other"
    if number.startswith("4"):
        return "Visa"
    two = int(number[:2])
    four = int(number[:4])
    if 51 <= two <= 55 or 2221 <= four <= 2720:
        return "MasterCard"
    return "Other"


def validate_phone_number(phone: str) -> bool:
    """
    Valida número telefónico mexicano (formato: +52 seguido de 10 dígitos).
    Acepta formatos: +521234567890, +52 123 456 7890, +52-123-456-7890
    """
    if not phone:
        return False
    # Normaliza: quita espacios, guiones y paréntesis
    normalized = re.sub(r"[\s\-()]+", "", phone)
    # Acepta +52 seguido de 10 dígitos o solo 10 dígitos
    return bool(re.fullmatch(r"\+52\d{10}|\d{10}", normalized))


# Mapeo mínimo (extiende cuando quieras)
BANK_CODE_MAP = {
    "001": "Banxico",
    "019": "Banjercito",
    "166": "Banco del bienestar",
    "002": "Banamex",
    "012": "BBVA México",
    "014": "Santander",
    "021": "HSBC",
    "030": "Ban Bajío",
    "036": "Inbursa",
    "042": "Mifel",
    "044": "Scotiabank",
    "058": "Banregio",
    "059": "Invex",
    "072": "Banorte",
    "113": "Ve por mas (B×+)",
    "127": "Banco Azteca",
    "130": "Compartamos Banco",
    "133": "Actinver",
    "137": "BanCoppel",
    "138": "Uala",
    "167": "Hey Banco",
    "638": "Nu",
    "646": "Sistema de Transferencia y Pagos (STP)",
    "661": "Klar",
    "699": "Fondeadora",
    "715": "Cashi",
    "722": "Mercado Pago",
    "728": "Spin by OXXO",
    # TODO: Keep updating bank codes
}

class BankDetails(models.Model):
    class Kind(models.TextChoices):
        PHONE = "PHONE", "Phone"
        CLABE = "CLABE", "CLABE"
        CARD = "CARD", "Card"
        ACCOUNT = "ACCOUNT", "Account"
    
    class Brand(models.TextChoices):
        VISA = "Visa", "Visa"
        MASTERCARD = "MasterCard", "MasterCard"
        OTHER = "Other", "Other"

    class BankNameSource(models.TextChoices):
        AUTO = "AUTO", "Auto-detected"
        MANUAL = "MANUAL", "Manual"
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bank_details",
    )

    kind = models.CharField(max_length=16, choices=Kind.choices)
    # Maximum length of numbers (CLABE=18, CARD=16, ACCOUNT flexible)
    value = models.CharField(max_length=32)

    bank_code = models.CharField(max_length=3, blank=True)
    bank_name = models.CharField(max_length=80, blank=True)
    bank_name_source = models.CharField(
        max_length=8, choices=BankNameSource.choices, default=BankNameSource.AUTO
    )

    brand = models.CharField(  # solo para CARD
        max_length=16, choices=Brand.choices, blank=True
    )

    alias = models.CharField(max_length=80, blank=True)
    
    # Número telefónico para WhatsApp (independiente del teléfono de registro)
    phone = models.CharField(max_length=20, blank=True, help_text="Registra tu numero para poder recibir tus comprobantes de pago")
    
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ✅ Only 1 per (owner, kind)
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "kind"], name="uniq_bankdetail_owner_kind"
            )
        ]
        indexes = [
            models.Index(fields=["owner", "kind"]),
        ]
        ordering = ("owner", "kind", "-updated_at")
    
    def __str__(self) -> str:
        return f"{self.owner} · {self.kind} · {self.masked_value}"
    
    # Normalize and validations

    def clean(self):
        # Normaliza: quita espacios y guiones del value
        if self.value:
            self.value = re.sub(r"[\s\-]+", "", self.value)

        # Valida y normaliza el número telefónico si está presente
        if self.phone:
            # Normaliza: quita espacios, guiones y paréntesis
            self.phone = re.sub(r"[\s\-()]+", "", self.phone)
            if not validate_phone_number(self.phone):
                raise ValidationError({"phone": "El número telefónico debe ser un número mexicano válido (10 dígitos o +52 seguido de 10 dígitos)."})
            # Asegura que siempre esté en formato +52XXXXXXXXXX
            if not self.phone.startswith("+52"):
                self.phone = f"+52{self.phone}"

        val = self.value or ""

        if self.kind == self.Kind.PHONE:
            # Para tipo PHONE, validamos el campo value como número telefónico
            if not val:
                raise ValidationError({"value": "El número de WhatsApp es requerido."})
            # Normaliza: quita espacios, guiones y paréntesis del value
            self.value = re.sub(r"[\s\-()]+", "", self.value)
            val = self.value
            if not validate_phone_number(val):
                raise ValidationError({"value": "El número telefónico debe ser un número mexicano válido (10 dígitos o +52 seguido de 10 dígitos)."})
            # Asegura que siempre esté en formato +52XXXXXXXXXX
            if not val.startswith("+52"):
                self.value = f"+52{val}"
            # Limpia campos que no aplican
            self.bank_code = ""
            self.bank_name = ""
            self.brand = ""
            self.phone = ""  # El número ya está en value

        elif self.kind == self.Kind.CLABE:
            if not re.fullmatch(r"\d{18}", val):
                raise ValidationError({"value": "La CLABE Interbancaria debe tener exactamente 18 dígitos."})
            if not clabe_checksum_ok(val):
                raise ValidationError({"value": "La CLABE Interbancaria no es válida."})

            self.bank_code = val[:3]
            # Autocompleta bank_name si está vacío o si está en modo AUTO
            suggestion = BANK_CODE_MAP.get(self.bank_code, "")
            if self.bank_name and self.bank_name.strip():
                self.bank_name_source = self.BankNameSource.MANUAL
            else:
                self.bank_name = suggestion
                self.bank_name_source = self.BankNameSource.AUTO

            # Marca no aplica
            self.brand = ""

        elif self.kind == self.Kind.CARD:
            if not re.fullmatch(r"\d{16}", val):
                raise ValidationError({"value": "El número de tarjeta debe tener exactamente 16 dígitos."})
            if not luhn_check(val):
                raise ValidationError({"value": "El número de tarjeta falló la verificación Luhn."})
            self.brand = detect_card_brand(val)
            # bank_code no aplica a tarjetas; limpia por si acaso
            self.bank_code = ""

        elif self.kind == self.Kind.ACCOUNT:
            if not re.fullmatch(r"\d{6,20}", val):
                raise ValidationError({"value": "El número de cuenta debe tener entre 6 y 20 dígitos."})
            # No hay autocompletado; respeta bank_name manual si existe
            self.bank_code = ""
            self.brand = ""

        else:
            raise ValidationError({"kind": "Tipo no soportado."})

    def save(self, *args, **kwargs):
        # Garantiza que clean() se ejecute al guardar (incluye normalización)
        self.full_clean()
        return super().save(*args, **kwargs)

    # ---- Utilidades de presentación -----------------------------------------
    @property
    def masked_value(self) -> str:
        """Representación enmascarada (para admin/UI interna)."""
        v = self.value or ""
        if not v:
            return ""
        if self.kind == self.Kind.PHONE:
            return v  # Muestra el número completo para WhatsApp
        if self.kind == self.Kind.CARD:
            return f"{'*' * 12}{v[-4:]}"  # **** **** **** 1234
        if self.kind == self.Kind.CLABE:
            return f"{v[:3]}{'*' * 12}{v[-3:]}"  # 123 ************ 456
        # ACCOUNT: muestra últimos 4
        return f"{'*' * max(0, len(v) - 4)}{v[-4:]}"