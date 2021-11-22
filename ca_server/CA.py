import random

from cryptography.hazmat.primitives import serialization
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
import datetime


class CA:
    def __init__(self):
        self.ca_privatekey= ec.generate_private_key(ec.SECP384R1())
        with open("CAkey.pem", "wb") as f2:
            f2.write(self.ca_privatekey.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(b"password"),
            ))
            f2.close()
        self.ca_name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u"CA"),
        ])
        self.crl = x509.CertificateRevocationListBuilder()
        self.crl = self.crl.issuer_name(self.ca_name)
        self.crl = self.crl.last_update(datetime.datetime.utcnow())
        self.crl = self.crl.next_update(datetime.datetime.utcnow().replace(day=datetime.datetime.utcnow().day+1))
        return

    # Issues certificate.
    # Requires name and public key (in PEM format) of individual who wants the certificate.
    # Returns the issued certificate in X.509 format as PEM file
    def issuecert(self, name, pk):
        clientkey = serialization.load_pem_public_key(pk)
        subject = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, name),
        ])
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            self.ca_name
        ).public_key(
            clientkey
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow().replace(year=datetime.datetime.utcnow().year+1)
        ).sign(self.ca_privatekey, hashes.SHA256())
        return cert.public_bytes(serialization.Encoding.PEM)

    # Revokes certificate using information provided by the datatbase (currently we assume the provided data consists of
    # serial number of the certificate to be revoked)
    # Returns serial nr
    def revokecert(self, serialnr):
        revokedcert = x509.RevokedCertificateBuilder().serial_number(
            serialnr
        ).revocation_date(
            datetime.datetime.today()
        ).build()
        self.crl = self.crl.add_revoked_certificate(revokedcert)
        self.crl = self.crl.last_update(datetime.datetime.utcnow())
        self.crl = self.crl.next_update(datetime.datetime.utcnow().replace(day=datetime.datetime.utcnow().day+1))
        return serialnr


    # Returns current CRL in PEM format
    def getCRL(self):
        return self.crl.sign(private_key=self.ca_privatekey, algorithm=hashes.SHA256()).public_bytes(serialization.Encoding.PEM)
