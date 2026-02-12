import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, X, MapPin, Tag, DollarSign, FileText, Image as ImageIcon } from 'lucide-react';
import Layout from '@/components/layout/Layout';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useToast } from '@/hooks/use-toast';
import { CATEGORIES, CAMPUS_LOCATIONS } from '@/data/mockData';
import { cn } from '@/lib/utils';

const CONDITIONS = ['Neuf', 'Comme neuf', 'Bon état', 'Usagé'] as const;

const Vendre = () => {
  const navigate = useNavigate();
  const { toast } = useToast();

  const [formData, setFormData] = useState({
    title: '',
    price: '',
    description: '',
    category: '',
    condition: '',
    location: '',
    courseCode: '',
  });
  const [images, setImages] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    // Simulate image upload with placeholder URLs
    const newImages = Array.from(files).map(
      (_, i) =>
        `https://images.unsplash.com/photo-${Date.now() + i}?w=400&h=300&fit=crop`
    );
    
    // For demo, use real placeholder images
    const placeholders = [
      'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop',
      'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400&h=300&fit=crop',
      'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop',
    ];

    setImages((prev) => [...prev, ...placeholders.slice(0, files.length)].slice(0, 5));
  };

  const removeImage = (index: number) => {
    setImages((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!formData.title || !formData.price || !formData.category || !formData.location) {
      toast({
        title: 'Champs requis manquants',
        description: 'Veuillez remplir tous les champs obligatoires.',
        variant: 'destructive',
      });
      return;
    }

    setIsSubmitting(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));

    toast({
      title: 'Annonce publiée !',
      description: 'Votre annonce est maintenant visible sur LavalMarket.',
    });

    setIsSubmitting(false);
    navigate('/catalogue');
  };

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-2xl md:text-3xl font-bold text-foreground mb-2">
              Vendre un article
            </h1>
            <p className="text-muted-foreground">
              Déposez votre annonce en quelques minutes
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Images */}
            <div className="space-y-4">
              <Label className="text-base font-semibold flex items-center gap-2">
                <ImageIcon className="w-5 h-5 text-primary" />
                Photos (max 5)
              </Label>
              
              <div className="grid grid-cols-3 sm:grid-cols-5 gap-3">
                {images.map((img, index) => (
                  <div
                    key={index}
                    className="relative aspect-square rounded-xl overflow-hidden border border-border bg-muted"
                  >
                    <img
                      src={img}
                      alt={`Upload ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                    <button
                      type="button"
                      onClick={() => removeImage(index)}
                      className="absolute top-1 right-1 w-6 h-6 rounded-full bg-destructive text-destructive-foreground flex items-center justify-center"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                ))}

                {images.length < 5 && (
                  <label className="aspect-square rounded-xl border-2 border-dashed border-border hover:border-primary/50 transition-colors cursor-pointer flex flex-col items-center justify-center gap-2 bg-muted/50">
                    <Upload className="w-6 h-6 text-muted-foreground" />
                    <span className="text-xs text-muted-foreground">Ajouter</span>
                    <input
                      type="file"
                      accept="image/*"
                      multiple
                      onChange={handleImageUpload}
                      className="hidden"
                    />
                  </label>
                )}
              </div>
            </div>

            {/* Title */}
            <div className="space-y-2">
              <Label htmlFor="title" className="text-base font-semibold flex items-center gap-2">
                <Tag className="w-5 h-5 text-primary" />
                Titre de l'annonce *
              </Label>
              <Input
                id="title"
                placeholder="Ex: Calculatrice TI-84 Plus CE"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="h-12"
              />
            </div>

            {/* Price */}
            <div className="space-y-2">
              <Label htmlFor="price" className="text-base font-semibold flex items-center gap-2">
                <DollarSign className="w-5 h-5 text-primary" />
                Prix *
              </Label>
              <div className="relative">
                <Input
                  id="price"
                  type="number"
                  placeholder="0"
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                  className="h-12 pr-12"
                />
                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground font-medium">
                  $
                </span>
              </div>
            </div>

            {/* Category & Condition */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-base font-semibold">Catégorie *</Label>
                <Select
                  value={formData.category}
                  onValueChange={(value) => setFormData({ ...formData, category: value })}
                >
                  <SelectTrigger className="h-12">
                    <SelectValue placeholder="Sélectionner" />
                  </SelectTrigger>
                  <SelectContent>
                    {CATEGORIES.map((cat) => (
                      <SelectItem key={cat.id} value={cat.id}>
                        <span className="flex items-center gap-2">
                          <span>{cat.icon}</span>
                          <span>{cat.label}</span>
                        </span>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-base font-semibold">État</Label>
                <Select
                  value={formData.condition}
                  onValueChange={(value) => setFormData({ ...formData, condition: value })}
                >
                  <SelectTrigger className="h-12">
                    <SelectValue placeholder="Sélectionner" />
                  </SelectTrigger>
                  <SelectContent>
                    {CONDITIONS.map((condition) => (
                      <SelectItem key={condition} value={condition}>
                        {condition}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Location */}
            <div className="space-y-2">
              <Label className="text-base font-semibold flex items-center gap-2">
                <MapPin className="w-5 h-5 text-primary" />
                Lieu de remise préféré *
              </Label>
              <Select
                value={formData.location}
                onValueChange={(value) => setFormData({ ...formData, location: value })}
              >
                <SelectTrigger className="h-12">
                  <SelectValue placeholder="Sélectionner un pavillon" />
                </SelectTrigger>
                <SelectContent>
                  {CAMPUS_LOCATIONS.map((location) => (
                    <SelectItem key={location} value={location}>
                      📍 {location}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Course Code (Optional) */}
            <div className="space-y-2">
              <Label htmlFor="courseCode" className="text-base font-semibold">
                Sigle de cours (optionnel)
              </Label>
              <Input
                id="courseCode"
                placeholder="Ex: GLO-2100, MAT-1900"
                value={formData.courseCode}
                onChange={(e) => setFormData({ ...formData, courseCode: e.target.value.toUpperCase() })}
                className="h-12"
              />
              <p className="text-sm text-muted-foreground">
                Ajoutez le sigle du cours si l'article est lié à un cours spécifique
              </p>
            </div>

            {/* Description */}
            <div className="space-y-2">
              <Label htmlFor="description" className="text-base font-semibold flex items-center gap-2">
                <FileText className="w-5 h-5 text-primary" />
                Description
              </Label>
              <Textarea
                id="description"
                placeholder="Décrivez votre article en détail..."
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="min-h-[120px] resize-none"
              />
            </div>

            {/* Submit */}
            <div className="pt-4">
              <Button
                type="submit"
                size="xl"
                className="w-full"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Publication en cours...' : 'Publier l\'annonce'}
              </Button>
              <p className="text-center text-sm text-muted-foreground mt-4">
                En publiant, vous acceptez les conditions d'utilisation de LavalMarket
              </p>
            </div>
          </form>
        </div>
      </div>
    </Layout>
  );
};

export default Vendre;
