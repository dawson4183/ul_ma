"""
DTO: RegisterRequestDto
Data Transfer Object pour la requête d'inscription.
"""
from dataclasses import dataclass


@dataclass
class RegisterRequestDto:
    """
    DTO contenant les données nécessaires pour une inscription.
    
    Attributs:
        email: Adresse email de l'utilisateur
        password: Mot de passe en clair (sera hashé)
        idul: Identifiant UL à 7 caractères
    """
    
    email: str
    password: str
    idul: str
