import os
import psycopg2

conn = psycopg2.connect(
        host="cataloguedb.xxxxxxx.rds.amazonaws.com",
        database="catalogue",
        user="devops",
        password="xxxxxx")

cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS products;')
cur.execute('CREATE TABLE products (id serial PRIMARY KEY,'
                             'description varchar (1000) NOT NULL,'
                             'image_url varchar (300) NOT NULL,'
                             'name varchar (150) NOT NULL,'
                             'date_added date DEFAULT CURRENT_TIMESTAMP);'
                             )

cur.execute('INSERT INTO products (description, image_url, name)'
            'VALUES (%s, %s, %s)',
            ('Behold the delicate elegance of this Origami Crane, rendered in soft pastel hues that lend it an ethereal charm. The graceful arch of its wings and the poised curvature of its neck evoke a sense of serenity and balance. Each meticulously folded crease tells a story of patience and precision, capturing the essence of the traditional art of paper folding. The gentle gradient of its pink hue enhances its beauty, reflecting the transient glow of a setting sun. This paper masterpiece serves as a poignant symbol of peace, hope, and the intricate dance of art and nature.',
             '/static/images/origami/001-origami.png',
             'Origami Crane (DB)')
            )

cur.execute('INSERT INTO products (description, image_url, name)'
            'VALUES (%s, %s, %s)',
            ('Dive into the enchanting realm of the Origami Frog, a captivating representation of the amphibious wonders that inhabit our ponds and wetlands. This artful creation, with its bulging eyes and poised, springy legs, encapsulates the playful essence and sprightly demeanor of its real-life counterpart. Crafted with meticulous precision, each fold and crease brings to life the frog\'s distinctive features, from its wide mouth to its textured back. Its poised stance, as if ready to leap into the next adventure, invites onlookers into a world where nature\'s simple joys come alive through the magic of paper folding. The Origami Frog stands not just as a testament to the art of origami, but also as a delightful ode to the vibrant and lively spirit of these charming aquatic creatures.',
             '/static/images/origami/012-origami-8.png',
             'Origami Frog (DB)')
            )

cur.execute('INSERT INTO products (description, image_url, name)'
            'VALUES (%s, %s, %s)',
            ('Step into the rugged landscapes of the Australian outback with our Origami Kangaroo, a masterful depiction of one of the continent\'s most iconic marsupials. This paper creation, with its powerful hind legs and distinctive pouch, captures the unique essence and agile grace of the kangaroo. Each fold and contour meticulously represents its muscular build, upright posture, and the gentle curve of its tail, used for balance during those impressive leaps. The attentive gaze and erect ears portray an ever-alert nature, characteristic of these fascinating creatures. Beyond its aesthetic allure, the Origami Kangaroo is also a symbol of strength, adaptability, and the boundless wonders of the natural world, all wrapped into a single, intricate piece of art.',
             '/static/images/origami/010-origami-6.png',
             'Origami Kangaroo (DB)')
            )

cur.execute('INSERT INTO products (description, image_url, name)'
            'VALUES (%s, %s, %s)',
            ('Journey into the sun-kissed dunes of the desert with our Origami Camel, a magnificent portrayal of the enduring giants that gracefully navigate the arid terrains. This artful masterpiece, with its humped back and long, graceful neck, perfectly encapsulates the camel\'s resilience and elegance. Each meticulous fold and crease gives life to its broad feet, adapted for sandy travels, and the gentle curve of its distinctive humps, which are nature\'s solution for long journeys without water. The poised stance and serene expression evoke images of golden horizons and the age-old tales of caravans that traverse vast landscapes under starry skies. The Origami Camel stands as a tribute to the majesty of these desert wanderers..',
             '/static/images/origami/021-camel.png',
             'Origami Camel (DB)')
            )

cur.execute('INSERT INTO products (description, image_url, name)'
            'VALUES (%s, %s, %s)',
            ('Witness the ephemeral beauty of our Origami Butterfly, a delicate creation symbolizing transformation and ethereal beauty. With wings that seem to flutter with an unspoken elegance, this piece allures eyes with its intricate patterns and gentle symmetries. Each fold carries with it a tale of metamorphosis, inviting you to embark upon a journey through blooming fields where these paper wonders flutter, leaving a trail of enchanted admirers in their gentle wake.',
             '/static/images/origami/017-origami-9.png',
             'Origami Butterfly (DB)')
            )

conn.commit()
cur.close()
conn.close()
