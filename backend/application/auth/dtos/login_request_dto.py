"""
DTO: LoginRequestDto
Data Transfer Object pour la requête de connexion.
"""
from dataclasses import dataclass


@dataclass
class LoginRequestDto:
    """
    DTO contenant les données nécessaires pour une connexion.
    
    Attributs:
        email: Adresse email de l'utilisateur
        password: Mot de passe en clair
    """
    
    email: str
    password: str
