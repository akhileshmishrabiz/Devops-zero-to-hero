package api

import (
	"github.com/gin-gonic/gin"
	"math/rand"
	"recommendation/data"  // replace with your actual project name
	"time"
)

func GetOrigamiOfTheDay(c *gin.Context) {
	origamis := data.GetDailyOrigami()
	rand.Seed(time.Now().Unix()) // initialize global pseudo random generator
	selectedOrigami := origamis[rand.Intn(len(origamis))] // get a random origami
	
	c.JSON(200, selectedOrigami)
}

func StartAPI() {
	r := gin.Default()
	r.GET("/origami-of-the-day", GetOrigamiOfTheDay)

	// TODO: Add more routes as needed
	
	r.Run(":8080")  // start the server on port 8080
}
