from django.db import models

from modelcluster.fields import ParentalKey, ForeignKey

from wagtail.models import Page, Orderable, ClusterableModel
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel


class HomePage(Page):
	tagline = RichTextField(blank=True)
	body = RichTextField(blank=True)
	max_count = 1 

	content_panels = Page.content_panels + [
		"tagline",
		"body",
		InlinePanel("card", label="Display Card"),
		]

	def get_context(self, request):
		context = super().get_context(request)
		context["cards"] = self.card.all().prefetch_related('links')
 
		# context["links"] = DisplayLink.objects.all()
		return context


class DisplayCard(Orderable, ClusterableModel):
	card_name = models.CharField(blank=True, max_length=250)
	page = ParentalKey("HomePage", related_name="card")


	panels = [
		FieldPanel("card_name"),
		InlinePanel("links", label="Page Links", max_num=3),
		]


class DisplayLink(Orderable):
	card = ParentalKey("DisplayCard", on_delete=models.CASCADE, related_name="links")
	link_name = models.CharField(blank=True, max_length=250)
	linked_page = models.ForeignKey('wagtailcore.Page', on_delete=models.SET_NULL, null=True, blank=True)
	link_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL, 
        related_name='+',
    )

	panels = [
		"link_name",
		PageChooserPanel("linked_page"),
		FieldPanel("link_image")
		]