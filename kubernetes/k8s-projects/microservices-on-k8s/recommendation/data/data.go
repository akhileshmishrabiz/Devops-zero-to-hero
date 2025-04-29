package data

type Origami struct {
	Name        string `json:"name"`
	Description string `json:"description"`
	ImageUrl    string `json:"image_url"`
}

func GetDailyOrigami() []Origami {
	return []Origami{
		{
			Name:        "Bird",
			Description: "Delight in the exquisite form of our Origami Bird of the Day, a splendid creation that speaks to the essence of finesse and simplicity in paper folding. Capturing the very spirit of freedom and poise, this avian origami is a visual treat, with its wings poised in mid-flight, inviting imaginations to soar across the endless skies. The graceful lines and carefully folded angles mirror the gentle curves of a bird in motion, transporting you to serene landscapes where these ethereal creatures dance with the wind.",
			ImageUrl:    "/static/images/origami/day1.png",
		},
		{
			Name:        "Rabbit",
			Description: "Embrace the whimsical world of our Origami Rabbit, an embodiment of gentleness and charm. With its perky ears attentively pricked and a subtle curvature in its poised posture, this paper art piece flawlessly mirrors the adorable and timid nature of the forest’s most enchanting dwellers. The intricate folds breathe life into the paper, providing it with a gentle, animated spirit that evokes images of lush meadows dotted with these delightful creatures, hopping joyously under the soft embrace of the spring sun.",
			ImageUrl:    "/static/images/origami/day2.png",
		},
		{
			Name:        "Dragon",
			Description: "Marvel at the mystical aura encapsulated within our Origami Dragon, a magical creature skillfully birthed from the delicate dance of paper and dexterous fingers. Fiery charisma and mythical grace emanate from each carefully molded wing and serpentine coil, transporting you to a fantastical realm where these magnificent beasts reign supreme, soaring amidst cloud-kissed peaks and enchanting our imaginations with tales of valor and epic adventures.",
			ImageUrl:    "/static/images/origami/day3.png",
		},
		{
			Name:        "Elephant",
			Description: "Our Origami Elephant stands as a majestic paper testament to the grandeur and gentle might of one of nature's most captivating giants. With a harmonious blend of intricate pleats and stable structures, the elephant origami illustrates a remarkable likeness to its real-world counterpart, encouraging admiration for its stately presence and the gentle wisdom reflected in its elegantly curved trunk and sturdy, grounded stance. It evokes a journey through the sprawling savannahs, where herds wander amidst golden grasses under a boundless azure sky.",
			ImageUrl:    "/static/images/origami/day4.png",
		},
		{
			Name:        "Cat",
			Description: "Lose yourself in the adorable and mischievous charm of our Origami Cat, a paper creation that perfectly encapsulates the playful spirit and sleek elegance of our feline friends. With eyes that gleam with curiosity and a poised, tactile structure, this delightful piece beckons you to step into a world where nimble paws prance in joyous abandon, and sleek tails flick with untold secrets and poised independence. The cat origami is a purr-fect blend of playful aesthetics and subtle complexity.",
			ImageUrl:    "/static/images/origami/day5.png",
		},
		{
			Name:        "Butterfly",
			Description: "Witness the ephemeral beauty of our Origami Butterfly, a delicate creation symbolizing transformation and ethereal beauty. With wings that seem to flutter with an unspoken elegance, this piece allures eyes with its intricate patterns and gentle symmetries. Each fold carries with it a tale of metamorphosis, inviting you to embark upon a journey through blooming fields where these paper wonders flutter, leaving a trail of enchanted admirers in their gentle wake.",
			ImageUrl:    "/static/images/origami/day6.png",
		},
		{
			Name:        "Windmill",
			Description: "Be swept away by the breezy elegance of our Origami Windmill, a symbol of sustainable energy and rustic charm. This timeless piece, with its rotating blades, captures the serene and perpetual motion powered by the invisible whispers of the wind. As it spins, it conjures images of sprawling fields of flowers, dotted with these kinetic sculptures, gently turning in a dance with nature, symbolizing a harmonious blend of tradition and future, where man and earth coexist in gentle symbiosis.",
			ImageUrl:    "/static/images/origami/day7.png",
		},
		// Add more origami objects here as desired.
	}
}
