"""
SOAP Address Validation Service — Module 4 Infrastructure
Spyne service providing address validation for Customer 360.
Deployed on ECS Fargate via Terraform, accessed by students' Mule flows via Web Service Consumer.
"""

import os
import re
from spyne import Application, ServiceBase, rpc, Unicode, Integer, Boolean, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# API Key authentication — when API_KEY env var is set, all requests except ?wsdl require it.
# When API_KEY is empty/unset, auth is skipped (local dev mode).
EXPECTED_API_KEY = os.environ.get("API_KEY", "")


class ApiKeyMiddleware:
    """WSGI middleware that checks X-API-Key header before passing to Spyne."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if not EXPECTED_API_KEY:
            return self.app(environ, start_response)

        # Allow WSDL requests without auth (students need to fetch the WSDL)
        query = environ.get("QUERY_STRING", "")
        if "wsdl" in query.lower():
            return self.app(environ, start_response)

        api_key = environ.get("HTTP_X_API_KEY", "")
        if api_key != EXPECTED_API_KEY:
            status = "403 Forbidden"
            body = b"<error>Invalid or missing API key</error>"
            headers = [("Content-Type", "text/xml"), ("Content-Length", str(len(body)))]
            start_response(status, headers)
            return [body]

        return self.app(environ, start_response)

# Known cities from our canonical customer data (high-confidence validation)
KNOWN_CITIES = {
    "austin", "san francisco", "boston", "seattle", "chicago",
    "detroit", "denver", "nashville", "portland", "charlotte"
}

# Valid US state abbreviations
VALID_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC"
}


class AddressValidationResult(ComplexModel):
    """Response type for ValidateAddress operation."""
    isValid = Boolean
    normalizedAddress = Unicode
    confidence = Integer


class AddressValidationService(ServiceBase):
    """SOAP service that validates and normalizes US addresses."""

    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=AddressValidationResult)
    def ValidateAddress(ctx, street, city, state, postalCode):
        """
        Validate a US address and return normalized form with confidence score.

        Args:
            street: Street address (e.g., "742 Evergreen Terrace")
            city: City name (e.g., "Austin")
            state: Two-letter state abbreviation (e.g., "TX")
            postalCode: 5-digit ZIP code (e.g., "78701")

        Returns:
            AddressValidationResult with isValid, normalizedAddress, confidence
        """
        result = AddressValidationResult()

        # Normalize inputs
        city_clean = (city or "").strip()
        state_clean = (state or "").strip().upper()
        street_clean = (street or "").strip().title()
        zip_clean = (postalCode or "").strip()

        # Build normalized address
        result.normalizedAddress = f"{street_clean}, {city_clean.title()}, {state_clean} {zip_clean}"

        # Validation logic
        is_known_city = city_clean.lower() in KNOWN_CITIES
        is_valid_state = state_clean in VALID_STATES
        is_valid_zip = bool(re.match(r"^\d{5}$", zip_clean))

        if is_known_city and is_valid_state and is_valid_zip:
            # Known city from our customer data — high confidence
            result.isValid = True
            # Vary confidence slightly based on city
            confidence_map = {
                "austin": 95, "san francisco": 92, "boston": 93,
                "seattle": 91, "chicago": 94, "detroit": 88,
                "denver": 90, "nashville": 89, "portland": 87,
                "charlotte": 86
            }
            result.confidence = confidence_map.get(city_clean.lower(), 85)
        elif is_valid_state and is_valid_zip:
            # Valid state + ZIP but unknown city — medium confidence
            result.isValid = True
            result.confidence = 70
        else:
            # Invalid data
            result.isValid = False
            result.confidence = 20

        return result


# Create SOAP application
application = Application(
    [AddressValidationService],
    tns="http://example.com/address",
    name="AddressService",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11()
)

_spyne_wsgi = WsgiApplication(application)
wsgi_app = ApiKeyMiddleware(_spyne_wsgi)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    print("\n" + "=" * 55)
    print("  SOAP Address Validation Service — MuleSoft Course")
    print("=" * 55)
    print("  WSDL: http://0.0.0.0:8091/?wsdl")
    print("  Operation: ValidateAddress(street, city, state, postalCode)")
    print("=" * 55 + "\n")

    server = make_server("0.0.0.0", 8091, wsgi_app)
    server.serve_forever()
