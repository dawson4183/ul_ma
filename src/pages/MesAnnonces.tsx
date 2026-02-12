import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Plus, Trash2, Eye, Package } from 'lucide-react';
import Layout from '@/components/layout/Layout';
import { Button } from '@/components/ui/button';
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
import { useListings } from '@/contexts/ListingsContext';
import LocationChip from '@/components/common/LocationChip';

// Simulation: l'utilisateur actuel est user-1
const CURRENT_USER_ID = 'user-1';

const MesAnnonces = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const { listings, deleteListing } = useListings();
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [listingToDelete, setListingToDelete] = useState<string | null>(null);

  // Filtrer les annonces de l'utilisateur actuel
  const myListings = listings.filter((listing) => listing.sellerId === CURRENT_USER_ID);

  const handleDeleteClick = (listingId: string) => {
    setListingToDelete(listingId);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = () => {
    if (listingToDelete) {
      deleteListing(listingToDelete);
      toast({
        title: 'Annonce supprimée',
        description: "L'annonce a été retirée du campus.",
      });
      setDeleteDialogOpen(false);
      setListingToDelete(null);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-CA', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-foreground">
              Mes Annonces
            </h1>
            <p className="text-muted-foreground mt-1">
              Gérez vos articles en vente
            </p>
          </div>
          <Link to="/vendre">
            <Button className="gap-2">
              <Plus className="w-4 h-4" />
              Nouvelle annonce
            </Button>
          </Link>
        </div>

        {/* Listings Grid */}
        {myListings.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {myListings.map((listing) => (
              <div
                key={listing.id}
                className="bg-card rounded-xl border border-border overflow-hidden shadow-card hover:shadow-card-hover transition-all"
              >
                {/* Image */}
                <div className="relative aspect-[4/3]">
                  <img
                    src={listing.images[0]}
                    alt={listing.title}
                    className="w-full h-full object-cover"
                  />
                  {listing.isSold && (
                    <div className="absolute inset-0 bg-foreground/60 flex items-center justify-center">
                      <span className="px-4 py-2 bg-card rounded-lg font-bold text-foreground">
                        VENDU
                      </span>
                    </div>
                  )}
                  <div className="absolute top-3 left-3">
                    <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-card/90 backdrop-blur-sm text-card-foreground">
                      {listing.condition}
                    </span>
                  </div>
                </div>

                {/* Content */}
                <div className="p-4 space-y-3">
                  <div>
                    <h3 className="font-semibold text-foreground line-clamp-2">
                      {listing.title}
                    </h3>
                    <p className="text-xl font-bold text-primary mt-1">
                      {listing.price}$
                    </p>
                  </div>

                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <LocationChip location={listing.location} />
                    <span>{formatDate(listing.createdAt)}</span>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2 pt-2">
                    <Link to={`/annonce/${listing.id}`} className="flex-1">
                      <Button variant="outline" size="sm" className="w-full gap-2">
                        <Eye className="w-4 h-4" />
                        Voir
                      </Button>
                    </Link>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDeleteClick(listing.id)}
                      className="text-destructive hover:text-destructive hover:bg-destructive/10"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="w-20 h-20 rounded-full bg-muted flex items-center justify-center mx-auto mb-4">
              <Package className="w-10 h-10 text-muted-foreground" />
            </div>
            <h3 className="text-xl font-semibold text-foreground mb-2">
              Aucune annonce
            </h3>
            <p className="text-muted-foreground mb-6">
              Vous n'avez pas encore publié d'annonces
            </p>
            <Link to="/vendre">
              <Button className="gap-2">
                <Plus className="w-4 h-4" />
                Créer ma première annonce
              </Button>
            </Link>
          </div>
        )}

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
                onClick={confirmDelete}
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

export default MesAnnonces;
