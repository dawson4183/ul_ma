import { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, MapPin, MessageCircle, Share2, Heart, Clock, User, Trash2 } from 'lucide-react';
import Layout from '@/components/layout/Layout';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { useToast } from '@/hooks/use-toast';
import VerifiedBadge from '@/components/common/VerifiedBadge';
import LocationChip from '@/components/common/LocationChip';
import { getUserById } from '@/data/mockData';
import { useListings } from '@/contexts/ListingsContext';

// Simulation: l'utilisateur actuel est user-1
const CURRENT_USER_ID = 'user-1';

const AnnoncePage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { toast } = useToast();
  const { getListingById, deleteListing, isListingDeleted } = useListings();
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  const listing = getListingById(id || '');
  const seller = listing ? getUserById(listing.sellerId) : undefined;
  const isOwner = listing?.sellerId === CURRENT_USER_ID;
  const isDeleted = isListingDeleted(id || '');

  const handleDeleteConfirm = () => {
    if (id) {
      deleteListing(id);
      toast({
        title: 'Annonce supprimée',
        description: "L'annonce a été retirée du campus.",
      });
      navigate('/mes-annonces');
    }
  };

  if (!listing || isDeleted) {
    return (
      <Layout>
        <div className="container mx-auto px-4 py-16 text-center">
          <h1 className="text-2xl font-bold text-foreground mb-4">
            Annonce introuvable
          </h1>
          <Link to="/catalogue">
            <Button variant="outline">Retour au catalogue</Button>
          </Link>
        </div>
      </Layout>
    );
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-CA', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    });
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        {/* Back Button */}
        <Link
          to="/catalogue"
          className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          Retour au catalogue
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          {/* Images - Left Side */}
          <div className="lg:col-span-3 space-y-4">
            {/* Main Image */}
            <div className="relative aspect-[4/3] rounded-2xl overflow-hidden bg-muted">
              <img
                src={listing.images[0]}
                alt={listing.title}
                className="w-full h-full object-cover"
              />
              
              {/* Badges */}
              <div className="absolute top-4 left-4 flex gap-2">
                <span className="px-3 py-1.5 rounded-full text-sm font-medium bg-card/90 backdrop-blur-sm text-card-foreground shadow-sm">
                  {listing.condition}
                </span>
                {listing.courseCode && (
                  <span className="px-3 py-1.5 rounded-full text-sm font-bold bg-primary text-primary-foreground shadow-md">
                    {listing.courseCode}
                  </span>
                )}
              </div>

              {/* Actions */}
              <div className="absolute top-4 right-4 flex gap-2">
                <Button variant="secondary" size="icon" className="rounded-full shadow-md">
                  <Heart className="w-4 h-4" />
                </Button>
                <Button variant="secondary" size="icon" className="rounded-full shadow-md">
                  <Share2 className="w-4 h-4" />
                </Button>
              </div>

              {listing.isSold && (
                <div className="absolute inset-0 bg-foreground/60 flex items-center justify-center">
                  <span className="px-6 py-3 bg-card rounded-xl font-bold text-xl text-foreground">
                    VENDU
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Details - Right Side */}
          <div className="lg:col-span-2 space-y-6">
            {/* Title & Price */}
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-foreground mb-3">
                {listing.title}
              </h1>
              <p className="text-3xl md:text-4xl font-extrabold text-primary">
                {listing.price}$
              </p>
            </div>

            {/* Location & Date */}
            <div className="flex flex-wrap items-center gap-3">
              <LocationChip location={listing.location} />
              <span className="flex items-center gap-1.5 text-sm text-muted-foreground">
                <Clock className="w-4 h-4" />
                {formatDate(listing.createdAt)}
              </span>
            </div>

            {/* Description */}
            <div className="bg-card rounded-xl border border-border p-4">
              <h2 className="font-semibold text-foreground mb-2">Description</h2>
              <p className="text-muted-foreground whitespace-pre-line">
                {listing.description}
              </p>
            </div>

            {/* Seller Info */}
            <div className="bg-card rounded-xl border border-border p-4">
              <div className="flex items-center gap-4">
                <Avatar className="w-14 h-14">
                  <AvatarImage src={seller?.avatar} />
                  <AvatarFallback>
                    <User className="w-6 h-6" />
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-foreground">
                      {seller?.name}
                    </span>
                    {seller?.isVerified && <VerifiedBadge />}
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {seller?.program}
                  </p>
                  <div className="flex items-center gap-4 mt-1">
                    <span className="text-sm text-muted-foreground">
                      ⭐ {seller?.rating}
                    </span>
                    <span className="text-sm text-muted-foreground">
                      {seller?.listingsCount} annonces
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* CTA */}
            <div className="space-y-3">
              {isOwner ? (
                <>
                  <Link to="/mes-annonces" className="block">
                    <Button variant="outline" size="xl" className="w-full">
                      Voir mes annonces
                    </Button>
                  </Link>
                  <Button
                    variant="ghost"
                    size="xl"
                    className="w-full gap-2 text-destructive hover:text-destructive hover:bg-destructive/10 border border-destructive/30"
                    onClick={() => setDeleteDialogOpen(true)}
                  >
                    <Trash2 className="w-5 h-5" />
                    Supprimer l'annonce
                  </Button>
                </>
              ) : (
                <>
                  <Link to="/messages" className="block">
                    <Button size="xl" className="w-full gap-2">
                      <MessageCircle className="w-5 h-5" />
                      Contacter le vendeur
                    </Button>
                  </Link>
                  <p className="text-center text-sm text-muted-foreground">
                    Rencontre sécurisée sur le campus
                  </p>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Delete Confirmation Dialog */}
        <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Supprimer l'annonce</AlertDialogTitle>
              <AlertDialogDescription>
                Êtes-vous sûr de vouloir supprimer cette annonce ? Cette action est
                irréversible et l'annonce sera retirée du campus définitivement.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Annuler</AlertDialogCancel>
              <AlertDialogAction
                onClick={handleDeleteConfirm}
                className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
              >
                Supprimer
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </Layout>
  );
};

export default AnnoncePage;
