import { useState, useEffect, useRef } from 'react';
import { Send, ArrowLeft, CheckCircle2, AlertTriangle } from 'lucide-react';
import Layout from '@/components/layout/Layout';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import VerifiedBadge from '@/components/common/VerifiedBadge';
import {
  mockConversations,
  mockMessages,
  getUserById,
  SMART_REPLY_LOCATIONS,
  Message,
  Conversation,
} from '@/data/mockData';
import { useListings } from '@/contexts/ListingsContext';
import { cn } from '@/lib/utils';

// Current user simulation
const CURRENT_USER_ID = 'user-1';

const Messages = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const { getListingById, isListingDeleted } = useListings();

  // Load conversations
  useEffect(() => {
    const timer = setTimeout(() => {
      setConversations(mockConversations);
      setIsLoading(false);
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  // Load messages for selected conversation
  useEffect(() => {
    if (selectedConversation) {
      const convMessages = mockMessages.filter(
        (m) => m.listingId === selectedConversation.listingId
      );
      setMessages(convMessages);
    }
  }, [selectedConversation]);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const getOtherParticipant = (conv: Conversation) => {
    const otherId = conv.participants.find((id) => id !== CURRENT_USER_ID);
    return getUserById(otherId || '');
  };

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim() || !selectedConversation) return;

    // Check if listing is deleted
    if (isListingDeleted(selectedConversation.listingId)) return;

    const newMsg: Message = {
      id: `msg-${Date.now()}`,
      senderId: CURRENT_USER_ID,
      receiverId: getOtherParticipant(selectedConversation)?.id || '',
      listingId: selectedConversation.listingId,
      content: newMessage,
      timestamp: new Date().toISOString(),
      isRead: false,
    };

    setMessages((prev) => [...prev, newMsg]);
    setNewMessage('');
  };

  const handleSmartReply = (location: string) => {
    if (selectedConversation && isListingDeleted(selectedConversation.listingId)) return;
    setNewMessage(`On se rejoint à : ${location} ?`);
  };

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('fr-CA', { hour: '2-digit', minute: '2-digit' });
  };

  // Check if current conversation's listing is deleted
  const isCurrentListingDeleted = selectedConversation 
    ? isListingDeleted(selectedConversation.listingId) 
    : false;

  return (
    <Layout>
      <div className="container mx-auto px-4 py-8">
        <div className="bg-card rounded-2xl border border-border shadow-card overflow-hidden h-[calc(100vh-12rem)]">
          <div className="flex h-full">
            {/* Conversations List */}
            <div
              className={cn(
                'w-full md:w-80 border-r border-border flex flex-col',
                selectedConversation ? 'hidden md:flex' : 'flex'
              )}
            >
              <div className="p-4 border-b border-border">
                <h1 className="text-xl font-bold text-foreground">Messages</h1>
              </div>

              <div className="flex-1 overflow-y-auto">
                {isLoading ? (
                  <div className="p-4 space-y-4">
                    {Array.from({ length: 3 }).map((_, i) => (
                      <div key={i} className="flex items-center gap-3 animate-pulse">
                        <div className="w-12 h-12 rounded-full skeleton-shimmer" />
                        <div className="flex-1 space-y-2">
                          <div className="h-4 skeleton-shimmer rounded w-3/4" />
                          <div className="h-3 skeleton-shimmer rounded w-1/2" />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : conversations.length > 0 ? (
                  <div className="divide-y divide-border">
                    {conversations.map((conv) => {
                      const otherUser = getOtherParticipant(conv);
                      const listing = getListingById(conv.listingId);
                      const listingDeleted = isListingDeleted(conv.listingId);
                      
                      return (
                        <button
                          key={conv.id}
                          onClick={() => setSelectedConversation(conv)}
                          className={cn(
                            'w-full p-4 flex items-start gap-3 hover:bg-secondary/50 transition-colors text-left',
                            selectedConversation?.id === conv.id && 'bg-secondary',
                            listingDeleted && 'opacity-60'
                          )}
                        >
                          <Avatar className="w-12 h-12">
                            <AvatarImage src={otherUser?.avatar} />
                            <AvatarFallback>
                              {otherUser?.name.charAt(0)}
                            </AvatarFallback>
                          </Avatar>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2">
                              <span className="font-semibold text-foreground truncate">
                                {otherUser?.name}
                              </span>
                              {otherUser?.isVerified && (
                                <VerifiedBadge showText={false} />
                              )}
                            </div>
                            <p className="text-sm text-muted-foreground truncate">
                              {listingDeleted ? (
                                <span className="text-destructive font-medium">Annonce supprimée</span>
                              ) : (
                                listing?.title
                              )}
                            </p>
                            <p className="text-sm text-muted-foreground truncate mt-1">
                              {conv.lastMessage}
                            </p>
                          </div>
                          {conv.unreadCount > 0 && !listingDeleted && (
                            <span className="flex items-center justify-center w-5 h-5 rounded-full bg-primary text-primary-foreground text-xs font-bold">
                              {conv.unreadCount}
                            </span>
                          )}
                        </button>
                      );
                    })}
                  </div>
                ) : (
                  <div className="p-8 text-center">
                    <p className="text-muted-foreground">
                      Aucune conversation pour le moment
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Chat Area */}
            <div
              className={cn(
                'flex-1 flex flex-col',
                !selectedConversation ? 'hidden md:flex' : 'flex'
              )}
            >
              {selectedConversation ? (
                <>
                  {/* Chat Header */}
                  <div className="p-4 border-b border-border">
                    <div className="flex items-center gap-3">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="md:hidden"
                        onClick={() => setSelectedConversation(null)}
                      >
                        <ArrowLeft className="w-5 h-5" />
                      </Button>

                      {/* Context Bar - Product Info */}
                      {(() => {
                        const listing = getListingById(selectedConversation.listingId);
                        const otherUser = getOtherParticipant(selectedConversation);
                        const listingDeleted = isListingDeleted(selectedConversation.listingId);
                        
                        return (
                          <div className="flex items-center gap-3 flex-1">
                            {listingDeleted ? (
                              <div className="w-12 h-12 rounded-lg bg-muted flex items-center justify-center">
                                <AlertTriangle className="w-5 h-5 text-muted-foreground" />
                              </div>
                            ) : (
                              <img
                                src={listing?.images[0]}
                                alt={listing?.title}
                                className="w-12 h-12 rounded-lg object-cover"
                              />
                            )}
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2">
                                <span className="font-semibold text-foreground">
                                  {otherUser?.name}
                                </span>
                                {otherUser?.isVerified && (
                                  <VerifiedBadge showText={false} />
                                )}
                              </div>
                              {listingDeleted ? (
                                <div className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-muted text-muted-foreground text-sm font-medium">
                                  <AlertTriangle className="w-3.5 h-3.5" />
                                  ANNONCE SUPPRIMÉE
                                </div>
                              ) : (
                                <p className="text-sm text-muted-foreground truncate">
                                  {listing?.title} · <span className="font-semibold text-primary">{listing?.price}$</span>
                                </p>
                              )}
                            </div>
                            {!listingDeleted && (
                              <Button variant="outline" size="sm" className="hidden sm:flex gap-1">
                                <CheckCircle2 className="w-4 h-4" />
                                Marquer Vendu
                              </Button>
                            )}
                          </div>
                        );
                      })()}
                    </div>
                  </div>

                  {/* Messages */}
                  <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {messages.map((msg) => {
                      const isOwn = msg.senderId === CURRENT_USER_ID;
                      return (
                        <div
                          key={msg.id}
                          className={cn(
                            'flex',
                            isOwn ? 'justify-end' : 'justify-start'
                          )}
                        >
                          <div
                            className={cn(
                              'max-w-[70%] px-4 py-2.5 rounded-2xl',
                              isOwn
                                ? 'bg-primary text-primary-foreground rounded-br-md'
                                : 'bg-secondary text-secondary-foreground rounded-bl-md'
                            )}
                          >
                            <p className="text-sm">{msg.content}</p>
                            <p
                              className={cn(
                                'text-xs mt-1',
                                isOwn
                                  ? 'text-primary-foreground/70'
                                  : 'text-muted-foreground'
                              )}
                            >
                              {formatTime(msg.timestamp)}
                            </p>
                          </div>
                        </div>
                      );
                    })}
                    <div ref={messagesEndRef} />
                  </div>

                  {/* Deleted Listing Notice or Smart Replies + Input */}
                  {isCurrentListingDeleted ? (
                    <div className="p-4 border-t border-border bg-muted/50">
                      <div className="flex items-center justify-center gap-2 text-muted-foreground">
                        <AlertTriangle className="w-4 h-4" />
                        <span className="text-sm">Cette annonce n'est plus disponible.</span>
                      </div>
                    </div>
                  ) : (
                    <>
                      {/* Smart Replies */}
                      <div className="px-4 pb-2">
                        <div className="flex flex-wrap gap-2">
                          {SMART_REPLY_LOCATIONS.map((location) => (
                            <button
                              key={location.label}
                              onClick={() => handleSmartReply(location.label)}
                              className="smart-reply-btn"
                            >
                              <span>{location.icon}</span>
                              <span>{location.label}</span>
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Message Input */}
                      <form
                        onSubmit={handleSendMessage}
                        className="p-4 border-t border-border"
                      >
                        <div className="flex items-center gap-2">
                          <Input
                            value={newMessage}
                            onChange={(e) => setNewMessage(e.target.value)}
                            placeholder="Écrire un message..."
                            className="flex-1"
                          />
                          <Button type="submit" size="icon" disabled={!newMessage.trim()}>
                            <Send className="w-4 h-4" />
                          </Button>
                        </div>
                      </form>
                    </>
                  )}
                </>
              ) : (
                <div className="flex-1 flex items-center justify-center">
                  <div className="text-center">
                    <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mx-auto mb-4">
                      <Send className="w-8 h-8 text-muted-foreground" />
                    </div>
                    <h3 className="font-semibold text-foreground mb-2">
                      Vos messages
                    </h3>
                    <p className="text-muted-foreground">
                      Sélectionnez une conversation pour commencer
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Messages;
