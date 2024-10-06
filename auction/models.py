from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

class AuctionListing(models.Model):
    CATEGORY_CHOICES = [ 
        ('PROTECCIONES', 'Protecciones'), 
        ('ENTRENAMIENTO', 'Entrenamiento'), 
        ('ROPA', 'Ropa'), 
        ('OTROS', 'Otros'), 
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    current_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    image = models.ImageField(upload_to='auction_images/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='OTHER')
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_auctions')
    
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    watchers = models.ManyToManyField(User, related_name='watchlist', blank=True)

    def add_to_watchlist(self, user):
        self.watchers.add(user)

    def remove_from_watchlist(self, user):
        self.watchers.remove(user)

    @property
    def watch_count(self):
        return self.watchers.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']

    @property
    def is_ended(self):
        return timezone.now() > self.end_date

    def place_bid(self, user, amount):
        """
        Place a bid on the auction.

        Args:
            user (User): The user placing the bid.
            amount (Decimal): The amount of the bid.

        Raises:
            ValueError: If the auction is not active or has ended.
            ValueError: If the bid is not higher than the current price.
        """
        if not self.is_active or self.is_ended:
            raise ValueError("This auction is not active or has ended.")
        if amount <= self.current_price:
            raise ValueError("Bid must be higher than the current price.")
        self.current_price = amount
        self.save()
        Bid.objects.create(auction=self, bidder=user, amount=amount)

    def add_comment(self, user, text):
        """
        Adds a comment to this auction listing.

        :param user: The User object who is making the comment
        :param text: The text content of the comment
        :return: The created Comment object
        """
        return Comment.objects.create(auction=self, user=user, text=text)

    @property
    def comment_count(self):
        """
        Returns the number of comments on this auction listing.
        """
        return self.comments.count()
    

class Comment(models.Model):
    """
    Model to represent comments on auction listings.
    """
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Show newest comments first

    def __str__(self):
        """String representation of the Comment object"""
        return f"Comment by {self.user.username} on {self.auction.title}"

    @property
    def is_edited(self):
        """
        Checks if the comment has been edited.
        """
        return self.created_at != self.updated_at

    def edit(self, new_text):
        """
        Edits the comment text.

        :param new_text: The new text for the comment
        """
        self.text = new_text
        self.save()

class Bid(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-amount']

    def __str__(self):
        return f"{self.bidder.username} bid ${self.amount} on {self.auction.title}"
    

class WatchList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_watchlist')
    items = models.ManyToManyField(AuctionListing, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Watchlist"

    def add_item(self, auction):
        self.items.add(auction)
        auction.add_to_watchlist(self.user)

    def remove_item(self, auction):
        self.items.remove(auction)
        auction.remove_from_watchlist(self.user)

    @property
    def item_count(self):
        return self.items.count()