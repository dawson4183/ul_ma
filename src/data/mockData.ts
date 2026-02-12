// Types pour le contrat API avec le backend Java Spring Boot
export interface User {
  id: string;
  name: string;
  program: string;
  email: string;
  avatar: string;
  isVerified: boolean;
  joinedDate: string;
  rating: number;
  listingsCount: number;
}

export interface Listing {
  id: string;
  title: string;
  price: number;
  description: string;
  category: string;
  condition: 'Neuf' | 'Comme neuf' | 'Bon état' | 'Usagé';
  images: string[];
  sellerId: string;
  location: string;
  courseCode?: string;
  createdAt: string;
  isSold: boolean;
}

export interface Message {
  id: string;
  senderId: string;
  receiverId: string;
  listingId: string;
  content: string;
  timestamp: string;
  isRead: boolean;
}

export interface Conversation {
  id: string;
  participants: string[];
  listingId: string;
  lastMessage: string;
  lastMessageTime: string;
  unreadCount: number;
}

// Lieux de rencontre officiels ULaval
export const CAMPUS_LOCATIONS = [
  'Pavillon Adrien-Pouliot',
  'Pavillon Desjardins',
  'Pavillon Charles-De Koninck',
  'PEPS',
  'Bibliothèque',
  'Pavillon Alexandre-Vachon',
] as const;

export const SMART_REPLY_LOCATIONS = [
  { label: 'Cafétéria Desjardins', icon: '☕' },
  { label: 'Entrée PEPS', icon: '🏃' },
  { label: 'Atrium Pouliot', icon: '📚' },
  { label: 'Bibliothèque', icon: '📖' },
] as const;

export const CATEGORIES = [
  { id: 'books', label: 'Livres', icon: '📚' },
  { id: 'electronics', label: 'Informatique', icon: '💻' },
  { id: 'housing', label: 'Appartements/Colocs', icon: '🏠' },
  { id: 'lab', label: 'Matériel de Labo', icon: '🔬' },
  { id: 'sports', label: 'Sports', icon: '⚽' },
  { id: 'clothing', label: 'Vêtements', icon: '👕' },
  { id: 'other', label: 'Autres', icon: '📦' },
] as const;

// Mock Users
export const mockUsers: User[] = [
  {
    id: 'user-1',
    name: 'Sophie Tremblay',
    program: 'Génie Logiciel',
    email: 'sophie.tremblay@ulaval.ca',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&h=150&fit=crop',
    isVerified: true,
    joinedDate: '2023-09-01',
    rating: 4.8,
    listingsCount: 12,
  },
  {
    id: 'user-2',
    name: 'Marc-Antoine Gagnon',
    program: 'Droit',
    email: 'marc-antoine.gagnon@ulaval.ca',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop',
    isVerified: true,
    joinedDate: '2022-01-15',
    rating: 4.9,
    listingsCount: 8,
  },
  {
    id: 'user-3',
    name: 'Émilie Roy',
    program: 'Médecine',
    email: 'emilie.roy@ulaval.ca',
    avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop',
    isVerified: true,
    joinedDate: '2023-01-10',
    rating: 5.0,
    listingsCount: 3,
  },
  {
    id: 'user-4',
    name: 'Alexandre Bouchard',
    program: 'Actuariat',
    email: 'alexandre.bouchard@ulaval.ca',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop',
    isVerified: false,
    joinedDate: '2024-01-05',
    rating: 4.5,
    listingsCount: 2,
  },
  {
    id: 'user-5',
    name: 'Camille Leblanc',
    program: 'Sciences Infirmières',
    email: 'camille.leblanc@ulaval.ca',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&h=150&fit=crop',
    isVerified: true,
    joinedDate: '2022-09-01',
    rating: 4.7,
    listingsCount: 15,
  },
];

// Mock Listings
export const mockListings: Listing[] = [
  {
    id: 'listing-1',
    title: 'Manuel Introduction à l\'Algorithmique (GLO-2100)',
    price: 45,
    description: 'Manuel en excellent état, quelques annotations au crayon. Obligatoire pour GLO-2100. Édition 2023.',
    category: 'books',
    condition: 'Bon état',
    images: ['https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=300&fit=crop'],
    sellerId: 'user-1',
    location: 'Pavillon Adrien-Pouliot',
    courseCode: 'GLO-2100',
    createdAt: '2024-01-15T10:00:00Z',
    isSold: false,
  },
  {
    id: 'listing-2',
    title: 'Calculatrice TI-84 Plus CE',
    price: 85,
    description: 'Calculatrice graphique parfaite pour MAT-1900 et STT-1000. Fonctionne parfaitement, vendue avec câble USB.',
    category: 'electronics',
    condition: 'Comme neuf',
    images: ['https://images.unsplash.com/photo-1564466809058-bf4114d55352?w=400&h=300&fit=crop'],
    sellerId: 'user-2',
    location: 'Pavillon Desjardins',
    courseCode: 'MAT-1900',
    createdAt: '2024-01-14T14:30:00Z',
    isSold: false,
  },
  {
    id: 'listing-3',
    title: 'iPad Air 4 - 64Go WiFi',
    price: 450,
    description: 'iPad Air 4ème génération, parfait pour prendre des notes. Inclut étui de protection et Apple Pencil 2ème gen.',
    category: 'electronics',
    condition: 'Bon état',
    images: ['https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop'],
    sellerId: 'user-3',
    location: 'Bibliothèque',
    createdAt: '2024-01-13T09:15:00Z',
    isSold: false,
  },
  {
    id: 'listing-4',
    title: 'Blouse de laboratoire chimie (Taille M)',
    price: 25,
    description: 'Blouse blanche 100% coton, obligatoire pour les labs de chimie. Portée une session seulement.',
    category: 'lab',
    condition: 'Bon état',
    images: ['https://images.unsplash.com/photo-1581093458791-9f3c3900df4b?w=400&h=300&fit=crop'],
    sellerId: 'user-3',
    location: 'Pavillon Alexandre-Vachon',
    createdAt: '2024-01-12T16:45:00Z',
    isSold: false,
  },
  {
    id: 'listing-5',
    title: 'Code Civil du Québec 2024',
    price: 65,
    description: 'Édition annotée 2024, indispensable pour les cours de droit civil. Aucune annotation.',
    category: 'books',
    condition: 'Neuf',
    images: ['https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400&h=300&fit=crop'],
    sellerId: 'user-2',
    location: 'Pavillon Charles-De Koninck',
    createdAt: '2024-01-11T11:20:00Z',
    isSold: false,
  },
  {
    id: 'listing-6',
    title: 'Chambre en colocation - Ste-Foy',
    price: 550,
    description: 'Chambre disponible dans un 5½ à 10 min à pied du campus. Colocs étudiants, ambiance studieuse. Disponible février.',
    category: 'housing',
    condition: 'Bon état',
    images: ['https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400&h=300&fit=crop'],
    sellerId: 'user-5',
    location: 'PEPS',
    createdAt: '2024-01-10T08:00:00Z',
    isSold: false,
  },
  {
    id: 'listing-7',
    title: 'Raquette de badminton Yonex',
    price: 40,
    description: 'Raquette légère, parfaite pour les cours au PEPS. Vendue avec housse et 3 volants.',
    category: 'sports',
    condition: 'Usagé',
    images: ['https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=400&h=300&fit=crop'],
    sellerId: 'user-4',
    location: 'PEPS',
    createdAt: '2024-01-09T13:30:00Z',
    isSold: false,
  },
  {
    id: 'listing-8',
    title: 'MacBook Pro 14" M2 Pro',
    price: 2200,
    description: 'MacBook Pro 2023, 16Go RAM, 512Go SSD. Parfait pour le développement. Batterie 95%. AppleCare+ jusqu\'en 2026.',
    category: 'electronics',
    condition: 'Comme neuf',
    images: ['https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=300&fit=crop'],
    sellerId: 'user-1',
    location: 'Pavillon Adrien-Pouliot',
    createdAt: '2024-01-08T10:00:00Z',
    isSold: false,
  },
];

// Mock Conversations
export const mockConversations: Conversation[] = [
  {
    id: 'conv-1',
    participants: ['user-1', 'user-2'],
    listingId: 'listing-2',
    lastMessage: 'Parfait, on se rejoint à la cafétéria Desjardins demain?',
    lastMessageTime: '2024-01-15T15:30:00Z',
    unreadCount: 2,
  },
  {
    id: 'conv-2',
    participants: ['user-1', 'user-3'],
    listingId: 'listing-3',
    lastMessage: 'Est-ce que l\'Apple Pencil est inclus?',
    lastMessageTime: '2024-01-15T12:00:00Z',
    unreadCount: 0,
  },
];

// Mock Messages
export const mockMessages: Message[] = [
  {
    id: 'msg-1',
    senderId: 'user-1',
    receiverId: 'user-2',
    listingId: 'listing-2',
    content: 'Salut! La calculatrice est-elle toujours disponible?',
    timestamp: '2024-01-15T14:00:00Z',
    isRead: true,
  },
  {
    id: 'msg-2',
    senderId: 'user-2',
    receiverId: 'user-1',
    listingId: 'listing-2',
    content: 'Oui, elle est toujours dispo! Tu veux la voir?',
    timestamp: '2024-01-15T14:15:00Z',
    isRead: true,
  },
  {
    id: 'msg-3',
    senderId: 'user-1',
    receiverId: 'user-2',
    listingId: 'listing-2',
    content: 'Super! On peut se rencontrer où sur le campus?',
    timestamp: '2024-01-15T15:00:00Z',
    isRead: true,
  },
  {
    id: 'msg-4',
    senderId: 'user-2',
    receiverId: 'user-1',
    listingId: 'listing-2',
    content: 'Parfait, on se rejoint à la cafétéria Desjardins demain?',
    timestamp: '2024-01-15T15:30:00Z',
    isRead: false,
  },
];

// Helper functions
export const getUserById = (id: string): User | undefined => 
  mockUsers.find(user => user.id === id);

export const getListingById = (id: string): Listing | undefined => 
  mockListings.find(listing => listing.id === id);

export const getListingsBySeller = (sellerId: string): Listing[] => 
  mockListings.filter(listing => listing.sellerId === sellerId);

export const getListingsByCategory = (category: string): Listing[] => 
  mockListings.filter(listing => listing.category === category);

export const searchListings = (query: string): Listing[] => {
  const lowerQuery = query.toLowerCase();
  return mockListings.filter(listing => 
    listing.title.toLowerCase().includes(lowerQuery) ||
    listing.description.toLowerCase().includes(lowerQuery) ||
    listing.courseCode?.toLowerCase().includes(lowerQuery)
  );
};
