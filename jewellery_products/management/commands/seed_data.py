import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from jewellery_products.models import Category, Product, Testimonial


class Command(BaseCommand):
    help = 'Seed database with dummy jewellery data using static images'

    def handle(self, *args, **options):
        # Create media directories
        media_products = settings.MEDIA_ROOT / 'products'
        media_products.mkdir(parents=True, exist_ok=True)
        media_categories = settings.MEDIA_ROOT / 'categories'
        media_categories.mkdir(parents=True, exist_ok=True)

        static_images = settings.BASE_DIR / 'static' / 'images'

        def copy_img(filename):
            src = static_images / filename
            dst = media_products / filename
            if src.exists() and not dst.exists():
                shutil.copy2(str(src), str(dst))
            return f'products/{filename}'

        def copy_cat_img(filename, cat_filename):
            src = static_images / filename
            dst = media_categories / cat_filename
            if src.exists():
                shutil.copy2(str(src), str(dst))
            return f'categories/{cat_filename}'

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        Testimonial.objects.all().delete()

        # ─── Categories ───────────────────────────────────────────────────
        self.stdout.write('Creating categories...')
        categories_data = [
            {
                'name': 'Necklaces',
                'description': 'Elegant gold and diamond necklaces for every occasion. From delicate chains to statement pieces crafted in Jaipur.',
                'img_src': 'j02.jpeg', 'img_dst': 'necklaces.jpeg',
            },
            {
                'name': 'Earrings',
                'description': 'Handcrafted earrings in gold, diamond, and precious stones. Studs, hoops, jhumkas, drops and more.',
                'img_src': 'j12.jpeg', 'img_dst': 'earrings.jpeg',
            },
            {
                'name': 'Rings',
                'description': 'Beautiful rings for every finger and every occasion. Solitaires, bands, cocktail rings and more.',
                'img_src': 'j22.jpeg', 'img_dst': 'rings.jpeg',
            },
            {
                'name': 'Bracelets',
                'description': 'Stunning gold and diamond bracelets. From delicate chains to bold bangles and kada sets.',
                'img_src': 'j32.jpeg', 'img_dst': 'bracelets.jpeg',
            },
            {
                'name': 'Anklets',
                'description': 'Delicate gold anklets and payal sets. Traditional and contemporary designs for graceful ankles.',
                'img_src': 'j40.jpeg', 'img_dst': 'anklets.jpeg',
            },
            {
                'name': 'Sets',
                'description': 'Complete jewellery sets for weddings and special occasions. Matching necklace, earring, ring and bangle sets.',
                'img_src': 'j45.jpeg', 'img_dst': 'sets.jpeg',
            },
        ]

        categories = {}
        for cat_data in categories_data:
            img_src = cat_data.pop('img_src')
            img_dst = cat_data.pop('img_dst')
            img_path = copy_cat_img(img_src, img_dst)
            cat = Category.objects.create(image=img_path, **cat_data)
            categories[cat.name] = cat
            self.stdout.write(f'  OK Category: {cat.name}')

        # ─── Products ─────────────────────────────────────────────────────
        self.stdout.write('Creating products...')
        products_data = [
            # NECKLACES (j01–j10)
            {
                'category': 'Necklaces', 'image': 'j01.jpeg',
                'name': 'Radiant Gold Choker',
                'description': 'A stunning 22K gold choker necklace adorned with intricate floral engravings. This handcrafted masterpiece features delicate filigree work inspired by the rich heritage of Jaipur. The adjustable length of 14–18 inches ensures a perfect fit. Perfect for weddings, festivals, and special occasions. Comes in a signature Trinora gift box with a certificate of authenticity.',
                'price': 24999, 'sale_price': 19999,
                'material': '22K Gold', 'is_featured': True,
            },
            {
                'category': 'Necklaces', 'image': 'j02.jpeg',
                'name': 'Diamond Drop Pendant',
                'description': 'A breathtaking 18K white gold pendant featuring a brilliant-cut solitaire diamond surrounded by a halo of smaller diamonds. The pendant hangs on an elegant 18-inch chain. GIA certified with SI1 clarity and G color grade. Total diamond weight 0.75 carats. An heirloom piece that will be treasured for generations.',
                'price': 45999,
                'material': '18K Gold, Diamond 0.75ct', 'is_featured': True,
            },
            {
                'category': 'Necklaces', 'image': 'j03.jpeg',
                'name': 'Emerald Gold Haaram',
                'description': 'A magnificent traditional haaram featuring vivid Colombian emeralds set in 22K gold. Each emerald is hand-selected for its rich green color and natural clarity. The intricate gold work features traditional peacock motifs. Total emerald weight 12 carats. A statement piece for brides and festive occasions.',
                'price': 89999,
                'material': '22K Gold, Colombian Emerald', 'is_featured': True,
            },
            {
                'category': 'Necklaces', 'image': 'j04.jpeg',
                'name': 'Pearl Layered Necklace',
                'description': 'A sophisticated three-layered necklace featuring hand-picked freshwater pearls strung on 18K gold chains. The gradient design moves from a single pearl at the top to a full strand at the bottom. Pearls measure 7–9mm with AAA luster rating. A timeless classic that works for both formal and casual occasions.',
                'price': 15999, 'sale_price': 12999,
                'material': '18K Gold, Freshwater Pearl', 'is_featured': True,
            },
            {
                'category': 'Necklaces', 'image': 'j05.jpeg',
                'name': 'Ruby Heart Pendant',
                'description': 'A romantic heart-shaped pendant featuring a vivid Burmese ruby set in 22K gold with a diamond halo. The pendant measures 18×16mm and hangs on a delicate 16-inch gold chain. Ruby weight: 1.2 carats. Diamond weight: 0.25 carats. A perfect gift of love for anniversaries and special occasions.',
                'price': 32999,
                'material': '22K Gold, Burmese Ruby, Diamond', 'is_featured': True,
            },
            {
                'category': 'Necklaces', 'image': 'j06.jpeg',
                'name': 'Temple Gold Necklace',
                'description': 'A regal temple-style necklace crafted in 22K gold featuring goddess motifs, ruby accents, and traditional antique finish. Inspired by the jewellery worn in South Indian temples. The main pendant measures 60×45mm. Perfect for classical dance performances, weddings, and religious ceremonies.',
                'price': 67999,
                'material': '22K Antique Gold, Ruby', 'is_featured': False,
            },
            {
                'category': 'Necklaces', 'image': 'j07.jpeg',
                'name': 'Diamond Tennis Necklace',
                'description': 'A glamorous tennis necklace featuring 52 brilliant-cut diamonds totaling 5 carats, set in polished 18K white gold. The prong setting maximizes each diamond\'s brilliance. Necklace length: 17 inches. Diamonds: VS2 clarity, F–G color. A classic jewellery piece that adds sparkle to any outfit, day or night.',
                'price': 125000, 'sale_price': 99999,
                'material': '18K White Gold, Diamond 5ct', 'is_featured': False,
            },
            {
                'category': 'Necklaces', 'image': 'j08.jpeg',
                'name': 'Antique Gold Mangalsutra',
                'description': 'A beautifully crafted traditional mangalsutra in 22K antique gold with black beads and a central pendant featuring Lakshmi motif. The pendant is set with polki diamonds and red enamel. Length: 18 inches adjustable. A sacred and beautiful symbol of matrimonial bliss.',
                'price': 28999,
                'material': '22K Antique Gold, Polki Diamond', 'is_featured': False,
            },
            {
                'category': 'Necklaces', 'image': 'j09.jpeg',
                'name': 'Rose Gold Twisted Chain',
                'description': 'A delicate and modern rose gold chain necklace with a subtle twisted rope design. Made from 18K rose gold, this versatile 20-inch piece can be worn alone or layered with other necklaces. Chain width: 2mm. The warm blush tone flatters all skin tones beautifully.',
                'price': 8999,
                'material': '18K Rose Gold', 'is_featured': False,
            },
            {
                'category': 'Necklaces', 'image': 'j10.jpeg',
                'name': 'Sapphire Floral Necklace',
                'description': 'A stunning floral design necklace featuring blue sapphires and diamonds set in 18K yellow gold. Five flower-shaped clusters are linked together in an elegant 16-inch arrangement. Total sapphire weight: 4 carats. Total diamond weight: 1 carat. The sapphires\' deep blue contrasts beautifully with warm gold.',
                'price': 54999,
                'material': '18K Gold, Sapphire, Diamond', 'is_featured': False,
            },
            # EARRINGS (j11–j20)
            {
                'category': 'Earrings', 'image': 'j11.jpeg',
                'name': 'Diamond Stud Earrings',
                'description': 'Classic and timeless 18K white gold stud earrings featuring round brilliant-cut diamonds totaling 1.0 carat. Set in secure four-prong settings for maximum light reflection. Diamond grade: VS1 clarity, E–F color. Post and butterfly back for secure wear. These versatile studs are perfect for everyday wear and special occasions alike.',
                'price': 34999,
                'material': '18K White Gold, Diamond 1ct', 'is_featured': True,
            },
            {
                'category': 'Earrings', 'image': 'j12.jpeg',
                'name': 'Gold Jhumka Earrings',
                'description': 'Traditional Rajasthani jhumka earrings in 22K gold with intricate filigree work and small ruby beads. The dome-shaped top leads to a gently swinging bell adorned with pearl drops. Earring length: 5.5cm. Weight: 12 grams per pair. These earrings make a musical, graceful statement at any ethnic occasion.',
                'price': 18999, 'sale_price': 14999,
                'material': '22K Gold, Ruby, Pearl', 'is_featured': True,
            },
            {
                'category': 'Earrings', 'image': 'j13.jpeg',
                'name': 'Emerald Drop Earrings',
                'description': 'Elegant drop earrings featuring pear-shaped Colombian emeralds suspended from 18K gold settings. Each emerald is surrounded by a halo of brilliant-cut diamonds. Emerald size: 9×6mm each. Total diamond weight: 0.6 carats. These earrings catch the light with every movement, creating a mesmerizing effect.',
                'price': 42999,
                'material': '18K Gold, Colombian Emerald, Diamond', 'is_featured': True,
            },
            {
                'category': 'Earrings', 'image': 'j14.jpeg',
                'name': 'Pearl Chandelier Earrings',
                'description': 'Luxurious chandelier earrings featuring cascading tiers of freshwater pearls and 22K gold links. The earrings measure 7cm in length and create a dramatic, feminine effect. Pearls: 5–7mm, AAA luster. Secure hook back with safety catch. Perfect for weddings, cocktail parties, and formal events.',
                'price': 12999,
                'material': '22K Gold, Freshwater Pearl', 'is_featured': False,
            },
            {
                'category': 'Earrings', 'image': 'j15.jpeg',
                'name': 'Ruby Hoop Earrings',
                'description': 'Statement hoop earrings in 18K gold featuring channel-set rubies. The hoops measure 35mm in diameter and are lightweight despite their bold appearance. Total ruby weight: 2 carats. The rubies create a continuous band of rich red color. Hinge-and-notch closure for security.',
                'price': 22999,
                'material': '18K Gold, Ruby 2ct', 'is_featured': False,
            },
            {
                'category': 'Earrings', 'image': 'j16.jpeg',
                'name': 'Polki Dangle Earrings',
                'description': 'Exquisite polki diamond dangle earrings in 22K gold with meenakari enamel work. These traditional earrings feature uncut diamonds in a floral pattern with colorful enamel on the reverse. Length: 6cm. Weight: 14 grams. A masterpiece of Indian craftsmanship showcasing centuries-old techniques.',
                'price': 38999, 'sale_price': 32999,
                'material': '22K Gold, Polki Diamond, Enamel', 'is_featured': True,
            },
            {
                'category': 'Earrings', 'image': 'j17.jpeg',
                'name': 'Sapphire Ear Cuffs',
                'description': 'Modern and edgy ear cuff earrings in 18K white gold with channel-set blue sapphires. These cuffs wrap elegantly around the ear without needing a piercing. Total sapphire weight: 0.8 carats. The contemporary design makes a bold fashion statement for the modern woman.',
                'price': 16999,
                'material': '18K White Gold, Sapphire', 'is_featured': False,
            },
            {
                'category': 'Earrings', 'image': 'j18.jpeg',
                'name': 'Rose Gold Pearl Studs',
                'description': 'Minimalist rose gold stud earrings featuring a single freshwater pearl set in an 18K rose gold bezel setting. Pearl size: 8mm, AAA luster. Post and butterfly back. The warm pearl-rose gold combination creates a delicate, romantic look. Perfect for everyday elegance in office and casual settings.',
                'price': 5999,
                'material': '18K Rose Gold, Freshwater Pearl', 'is_featured': False,
            },
            {
                'category': 'Earrings', 'image': 'j19.jpeg',
                'name': 'Temple Kasumala Earrings',
                'description': 'Traditional South Indian temple earrings in 22K gold featuring goddess Lakshmi motifs. The earrings have a distinctive long drop design with multiple tiers and small gold beads. Length: 8cm. These stunning pieces are perfect for classical dance, religious ceremonies, and traditional weddings.',
                'price': 29999,
                'material': '22K Gold', 'is_featured': False,
            },
            {
                'category': 'Earrings', 'image': 'j20.jpeg',
                'name': 'Diamond Flower Earrings',
                'description': 'Beautiful flower-shaped stud earrings in 18K gold with a central diamond surrounded by petals of smaller diamonds. Each flower measures 12mm in diameter. Total diamond weight: 0.8 carats, VS2 clarity, F color. Secure screw-back posts. A perfect gift for birthdays, anniversaries, and celebrations.',
                'price': 48999,
                'material': '18K Gold, Diamond 0.8ct', 'is_featured': False,
            },
            # RINGS (j21–j30)
            {
                'category': 'Rings', 'image': 'j21.jpeg',
                'name': 'Solitaire Diamond Ring',
                'description': 'The ultimate symbol of love — a classic solitaire ring featuring a round brilliant-cut diamond of 1.5 carats set in a six-prong 18K white gold setting. GIA certified with VS1 clarity and E color. Ring width: 2.5mm. Available in sizes 5–10. The timeless design ensures this ring will never go out of style.',
                'price': 149999,
                'material': '18K White Gold, Diamond 1.5ct GIA', 'is_featured': True,
            },
            {
                'category': 'Rings', 'image': 'j22.jpeg',
                'name': 'Emerald Cocktail Ring',
                'description': 'A stunning cocktail ring featuring a 3-carat Colombian emerald surrounded by a halo of brilliant diamonds in 18K yellow gold. The emerald measures 10×8mm oval cut. Diamond weight: 0.8 carats. Emerald is Zambian origin with minor oil treatment. This ring commands attention in any room.',
                'price': 89999, 'sale_price': 74999,
                'material': '18K Gold, Emerald 3ct, Diamond', 'is_featured': True,
            },
            {
                'category': 'Rings', 'image': 'j23.jpeg',
                'name': 'Engraved Gold Band',
                'description': 'A beautifully crafted 22K gold band ring with delicate hand-engraved floral patterns. The 4mm wide band is comfortable for everyday wear. Weight: approximately 5 grams. Available in sizes 5–12. The warm yellow gold catches the light magnificently with every gesture. A classic piece for every collection.',
                'price': 9999,
                'material': '22K Gold', 'is_featured': False,
            },
            {
                'category': 'Rings', 'image': 'j24.jpeg',
                'name': 'Ruby Cluster Ring',
                'description': 'A vibrant cluster ring featuring Burmese rubies and diamonds in an 18K gold setting. Central oval ruby: 1.5 carats. Surrounding: 12 smaller rubies totaling 1 carat and 24 diamond accents of 0.3 carats. A bold, colorful statement piece for cocktail parties and special occasions.',
                'price': 62999,
                'material': '18K Gold, Burmese Ruby, Diamond', 'is_featured': True,
            },
            {
                'category': 'Rings', 'image': 'j25.jpeg',
                'name': 'Rose Gold Diamond Band',
                'description': 'A romantic eternity band in 18K rose gold with channel-set round brilliant diamonds. Total diamond weight: 2 carats, VS1 clarity, F–G color. Band width: 3mm. The rose gold\'s warm blush tone makes the diamonds appear larger and more brilliant. Perfect as a wedding band or anniversary gift.',
                'price': 54999,
                'material': '18K Rose Gold, Diamond 2ct', 'is_featured': False,
            },
            {
                'category': 'Rings', 'image': 'j26.jpeg',
                'name': 'Polki Statement Ring',
                'description': 'A magnificent statement ring featuring uncut polki diamonds set in 22K gold with intricate meenakari work on the reverse. The top surface is covered with polki diamonds in a floral arrangement measuring 25×20mm. A true collector\'s piece reflecting India\'s finest jewellery tradition.',
                'price': 44999, 'sale_price': 39999,
                'material': '22K Gold, Polki Diamond, Enamel', 'is_featured': False,
            },
            {
                'category': 'Rings', 'image': 'j27.jpeg',
                'name': 'Sapphire Three Stone Ring',
                'description': 'A classic three-stone ring in 18K white gold featuring a central blue sapphire flanked by two oval-cut diamonds. This design symbolizes the past, present, and future. Central sapphire: 2 carats, 8×6mm. Diamond weight: 0.6 carats. GIA certified. Available in sizes 4–10.',
                'price': 78999,
                'material': '18K White Gold, Sapphire, Diamond', 'is_featured': False,
            },
            {
                'category': 'Rings', 'image': 'j28.jpeg',
                'name': 'Kundan Floral Ring',
                'description': 'A traditional Rajasthani kundan ring featuring a central flower design with colored gemstones set in 22K gold. The ring features blue, green, and red stones in a vibrant floral pattern with gold scrollwork. Ring width: 18mm at widest. A wearable piece of art from Jaipur\'s finest artisans.',
                'price': 18999,
                'material': '22K Gold, Kundan, Gemstones', 'is_featured': False,
            },
            {
                'category': 'Rings', 'image': 'j29.jpeg',
                'name': 'Diamond Infinity Ring',
                'description': 'A modern infinity ring in 18K white gold with pavé-set diamonds forming the infinity symbol. Total diamond weight: 0.5 carats, SI1 clarity, G color. Band width: 8mm at widest. This ring represents eternal love and infinite possibilities. Available in sizes 4–10.',
                'price': 29999,
                'material': '18K White Gold, Diamond 0.5ct', 'is_featured': False,
            },
            {
                'category': 'Rings', 'image': 'j30.jpeg',
                'name': 'Vintage Pearl Ring',
                'description': 'A vintage-inspired ring featuring a baroque freshwater pearl set in an elaborate 22K gold setting with diamond accents. Pearl size: 12×10mm. Diamond weight: 0.15 carats. The ornate setting features scrollwork and milgrain details reminiscent of Edwardian jewellery. A romantic and unique piece.',
                'price': 14999,
                'material': '22K Gold, Baroque Pearl, Diamond', 'is_featured': False,
            },
            # BRACELETS (j31–j38)
            {
                'category': 'Bracelets', 'image': 'j31.jpeg',
                'name': 'Gold Kangan Bangle Set',
                'description': 'Traditional 22K gold kangan bangles with a diameter of 62mm, featuring intricate wire-twist designs and small diamond-cut beads. Sold as a set of two. Weight: 18 grams each. The substantial weight makes these bangles feel luxuriously premium. A festive season staple.',
                'price': 34999,
                'material': '22K Gold', 'is_featured': True,
            },
            {
                'category': 'Bracelets', 'image': 'j32.jpeg',
                'name': 'Diamond Tennis Bracelet',
                'description': 'A classic tennis bracelet in 18K white gold featuring 28 prong-set round brilliant diamonds totaling 3.5 carats. VS2 clarity, F–G color. Length: 7 inches with box clasp and safety catch. The flexible design ensures comfortable wear. Perfect for formal occasions or as a luxurious everyday piece.',
                'price': 89999, 'sale_price': 79999,
                'material': '18K White Gold, Diamond 3.5ct', 'is_featured': True,
            },
            {
                'category': 'Bracelets', 'image': 'j33.jpeg',
                'name': 'Ruby Bangle Set',
                'description': 'A set of three 22K gold bangles with channel-set rubies. Each bangle is 4mm wide and features rubies of 2mm diameter. Diameter: 62mm. These colorful bangles look stunning worn individually or stacked together. Perfect for Diwali, Navratri, and all festive occasions.',
                'price': 28999,
                'material': '22K Gold, Ruby', 'is_featured': False,
            },
            {
                'category': 'Bracelets', 'image': 'j34.jpeg',
                'name': 'Rose Gold Charm Bracelet',
                'description': 'A delightful 18K rose gold charm bracelet featuring six hand-crafted charms including a star, heart, moon, key, flower, and butterfly. Each charm measures approximately 12mm. Length: 7 inches with lobster clasp. New charms can be added to celebrate special moments. A gift that grows with memories.',
                'price': 16999,
                'material': '18K Rose Gold', 'is_featured': False,
            },
            {
                'category': 'Bracelets', 'image': 'j35.jpeg',
                'name': 'Polki Bridal Bangle',
                'description': 'A magnificent broad bangle in 22K gold featuring uncut polki diamonds set in kundan style. Width: 25mm. Diameter: 62mm. The elaborate floral pattern is studded with polki diamonds of various sizes. Meenakari enamel work on the reverse adds a beautiful finishing touch. A bridal showstopper.',
                'price': 124999,
                'material': '22K Gold, Polki Diamond, Enamel', 'is_featured': True,
            },
            {
                'category': 'Bracelets', 'image': 'j36.jpeg',
                'name': 'Sapphire Link Bracelet',
                'description': 'A sophisticated link bracelet in 18K yellow gold featuring alternating sapphire and diamond links. Length: 7 inches with box clasp. Total sapphire weight: 2 carats. Total diamond weight: 0.5 carats. The alternating pattern creates a beautiful rhythm of blue and white sparkle.',
                'price': 45999, 'sale_price': 38999,
                'material': '18K Gold, Sapphire, Diamond', 'is_featured': False,
            },
            {
                'category': 'Bracelets', 'image': 'j37.jpeg',
                'name': 'Pearl Strand Bracelet',
                'description': 'An elegant single-strand bracelet featuring 18 matched freshwater pearls with a 22K gold box clasp set with a small diamond. Pearls: 8mm diameter, AAA luster, minimal blemishes. Length: 7 inches. The pearls are hand-knotted between each pearl to prevent loss. A timeless classic.',
                'price': 11999,
                'material': '22K Gold, Freshwater Pearl', 'is_featured': False,
            },
            {
                'category': 'Bracelets', 'image': 'j38.jpeg',
                'name': 'Engraved Gold Kada',
                'description': 'A bold and beautiful 22K gold kada (broad bangle) with intricate floral engravings and a spiral design. Diameter: 60mm. Width: 20mm. Weight: approximately 40 grams. This single bangle makes a strong statement at any occasion. A must-have addition to every jewellery wardrobe.',
                'price': 52999,
                'material': '22K Gold', 'is_featured': False,
            },
            # ANKLETS (j39–j44)
            {
                'category': 'Anklets', 'image': 'j39.jpeg',
                'name': 'Traditional Payal Set',
                'description': 'A pair of traditional 22K gold payal (anklets) featuring delicate chain work with small ghunghru (bells) that make a soft, melodic sound with every step. Each anklet: 25cm length. Safety clasp. Weight: 8 grams per anklet. The sound of gold payal is the sound of timeless elegance.',
                'price': 22999,
                'material': '22K Gold', 'is_featured': True,
            },
            {
                'category': 'Anklets', 'image': 'j40.jpeg',
                'name': 'Diamond Anklet',
                'description': 'A modern and glamorous anklet in 18K white gold with prong-set diamonds. The anklet features 24 round brilliant-cut diamonds totaling 0.5 carats. VS1 clarity, F color. Length: 10 inches with lobster clasp and 1-inch extender. This luxurious piece elevates any outfit and draws attention to graceful ankles.',
                'price': 34999, 'sale_price': 28999,
                'material': '18K White Gold, Diamond 0.5ct', 'is_featured': True,
            },
            {
                'category': 'Anklets', 'image': 'j41.jpeg',
                'name': 'Gold Bead Anklet',
                'description': 'A charming anklet in 22K gold featuring alternating smooth and diamond-cut beads. Length: 26cm with lobster clasp. Weight: 4 grams. The varied bead sizes (3mm and 5mm) create a playful, textural look. Suitable for everyday wear and festive occasions.',
                'price': 8999,
                'material': '22K Gold', 'is_featured': False,
            },
            {
                'category': 'Anklets', 'image': 'j42.jpeg',
                'name': 'Ruby Gold Anklet',
                'description': 'A vibrant gold anklet featuring small ruby beads interspersed between gold links. The 22K gold chain with 18 round rubies (2mm each) creates a colorful pop of red against the ankles. Length: 25cm. Perfect for ethnic wear, sarees, and festive celebrations.',
                'price': 14999,
                'material': '22K Gold, Ruby', 'is_featured': False,
            },
            {
                'category': 'Anklets', 'image': 'j43.jpeg',
                'name': 'Butterfly Charm Anklet',
                'description': 'A whimsical 18K rose gold anklet featuring three-dimensional butterfly charms at regular intervals. Each butterfly is pavé-set with tiny diamonds. Total diamond weight: 0.2 carats. Length: 10 inches. The delicate chain connects the butterflies in a light, airy design perfect for summer and beach weddings.',
                'price': 18999,
                'material': '18K Rose Gold, Diamond', 'is_featured': False,
            },
            {
                'category': 'Anklets', 'image': 'j44.jpeg',
                'name': 'Ghunghru Payal Set',
                'description': 'A classic pair of 22K gold ghunghru anklets featuring multiple layers of tiny bells that create beautiful music with every step. The broad design (width: 20mm) features intricate gold work and 48 tiny bells per anklet. Length: 25cm. Beloved by classical dancers, brides, and jewellery collectors.',
                'price': 41999, 'sale_price': 34999,
                'material': '22K Gold', 'is_featured': False,
            },
            # SETS (j45–j51)
            {
                'category': 'Sets', 'image': 'j45.jpeg',
                'name': 'Bridal Grand Set',
                'description': 'The complete bridal jewellery package featuring a magnificent 22K gold necklace, matching jhumka earrings, maang tikka, and hand harness. The set features rubies, emeralds, and polki diamonds in traditional Rajasthani style. Total gold weight: approximately 120 grams. Your perfect wedding day companion.',
                'price': 299999,
                'material': '22K Gold, Ruby, Emerald, Polki Diamond', 'is_featured': True,
            },
            {
                'category': 'Sets', 'image': 'j46.jpeg',
                'name': 'Diamond Necklace Earring Set',
                'description': 'An elegant diamond jewellery set in 18K white gold featuring a graduated diamond necklace and matching stud earrings. Necklace length: 17 inches with 21 brilliant-cut diamonds. Earring diamonds: 0.5 carats each. Total diamond weight: 3.5 carats. VS2 clarity, F–G color.',
                'price': 185000, 'sale_price': 159999,
                'material': '18K White Gold, Diamond 3.5ct', 'is_featured': True,
            },
            {
                'category': 'Sets', 'image': 'j47.jpeg',
                'name': 'Pearl Complete Jewellery Set',
                'description': 'A sophisticated pearl jewellery set including a 3-strand pearl necklace (17 inches), pearl drop earrings, and pearl bracelet (7 inches). All pieces feature hand-selected freshwater pearls of matching size (8mm) and luster strung on 18K gold findings. Elegant and timeless.',
                'price': 42999,
                'material': '18K Gold, Freshwater Pearl', 'is_featured': False,
            },
            {
                'category': 'Sets', 'image': 'j48.jpeg',
                'name': 'Emerald Jewellery Set',
                'description': 'A dazzling set featuring a Colombian emerald and diamond necklace, matching drop earrings, and cocktail ring in 18K yellow gold. Total emerald weight: 8 carats. Total diamond weight: 2 carats. A complete green-gold statement for gala events, cocktail parties, and celebrations.',
                'price': 235000,
                'material': '18K Gold, Colombian Emerald 8ct, Diamond 2ct', 'is_featured': False,
            },
            {
                'category': 'Sets', 'image': 'j49.jpeg',
                'name': 'Daily Wear Gold Set',
                'description': 'A practical and beautiful everyday jewellery set in 22K gold including a delicate chain necklace (18 inches), small hoop earrings (20mm diameter), and a slim bangle (62mm). Each piece is designed to be light and comfortable for daily wear while still looking polished and elegant.',
                'price': 28999,
                'material': '22K Gold', 'is_featured': False,
            },
            {
                'category': 'Sets', 'image': 'j50.jpeg',
                'name': 'Rose Gold Trio Set',
                'description': 'A romantic rose gold set in 18K gold including a floral pendant necklace (16 inches), matching pavé stud earrings, and a thin eternity band. Each piece features pavé-set diamonds in a shared floral design language. Total diamond weight: 0.6 carats. A perfect gift for a loved one.',
                'price': 45999, 'sale_price': 38999,
                'material': '18K Rose Gold, Diamond 0.6ct', 'is_featured': True,
            },
            {
                'category': 'Sets', 'image': 'j51.jpeg',
                'name': 'Kundan Bridal Set',
                'description': 'An opulent kundan bridal set featuring a layered necklace, jhumka earrings, maang tikka, and a set of four bangles in 22K gold with kundan work, pearls, and meenakari enamel. Total gold weight: approximately 90 grams. This set is the embodiment of royal Indian bridal tradition.',
                'price': 189999,
                'material': '22K Gold, Kundan, Pearl, Enamel', 'is_featured': True,
            },
        ]

        for p_data in products_data:
            cat_name = p_data.pop('category')
            img_name = p_data.pop('image')
            img_path = copy_img(img_name)
            Product.objects.create(
                category=categories[cat_name],
                image=img_path,
                **p_data
            )

        # ─── Testimonials ─────────────────────────────────────────────────
        self.stdout.write('Creating testimonials...')
        testimonials_data = [
            {
                'name': 'Priya Sharma',
                'location': 'Mumbai, Maharashtra',
                'text': 'I purchased the Bridal Grand Set for my wedding and received so many compliments! The quality is exceptional and the craftsmanship is breathtaking. Trinora\'s packaging is also stunning — felt like opening a treasure chest. Will shop here for all my jewellery needs!',
                'rating': 5, 'is_active': True,
            },
            {
                'name': 'Ananya Reddy',
                'location': 'Hyderabad, Telangana',
                'text': 'The Diamond Tennis Necklace I ordered arrived beautifully packaged and exactly as described. The diamonds are brilliant and the setting is flawless. Customer service was extremely helpful in choosing the right piece. Five stars without hesitation!',
                'rating': 5, 'is_active': True,
            },
            {
                'name': 'Kavitha Nair',
                'location': 'Kochi, Kerala',
                'text': 'Ordered the Gold Jhumka Earrings as a birthday gift for my mother. She absolutely loves them! The traditional craftsmanship reminds her of her grandmother\'s jewellery. Trinora has truly captured the essence of Indian jewellery while keeping it fresh and modern.',
                'rating': 5, 'is_active': True,
            },
            {
                'name': 'Deepika Agarwal',
                'location': 'Jaipur, Rajasthan',
                'text': 'The Polki Statement Ring is an absolute masterpiece. I was hesitant ordering such an expensive piece online but the certificate of authenticity and detailed photos gave me confidence. It looks even better in person! The gift packaging was exquisite.',
                'rating': 5, 'is_active': True,
            },
            {
                'name': 'Meera Patel',
                'location': 'Ahmedabad, Gujarat',
                'text': 'Fast shipping, beautiful packaging, and the Pearl Layered Necklace exceeded my expectations. The pearls are perfectly matched and the gold quality is excellent. Trinora has earned a loyal customer for life. Already planning my next purchase!',
                'rating': 5, 'is_active': True,
            },
        ]

        for t_data in testimonials_data:
            Testimonial.objects.create(**t_data)

        self.stdout.write(self.style.SUCCESS(
            f'\nDatabase seeded successfully!\n'
            f'   Categories   : {Category.objects.count()}\n'
            f'   Products     : {Product.objects.count()}\n'
            f'   Testimonials : {Testimonial.objects.count()}\n'
        ))
