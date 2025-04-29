package main

import (
	"github.com/gin-gonic/gin"
        "recommendation/api"
	"net/http"
	"time"
        "encoding/json"
	"net"
        "os"
)


// Config represents the structure of our configuration file.
type Config struct {
    Version string `json:"version"`
}

// loadConfig reads the configuration file and returns a Config struct.
func loadConfig() (Config, error) {
    file, err := os.Open("config.json")
    if err != nil {
        return Config{}, err
    }
    defer file.Close()

    config := Config{}
    decoder := json.NewDecoder(file)
    err = decoder.Decode(&config)
    return config, err
}


type SystemInfo struct {
	Hostname      string
	IPAddress     string
	IsContainer   bool
	IsKubernetes  bool
}

func GetSystemInfo() SystemInfo {
	hostname, _ := os.Hostname()
	addrs, _ := net.InterfaceAddrs()
	ip := ""
	for _, addr := range addrs {
		if ipnet, ok := addr.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				ip = ipnet.IP.String()
				break
			}
		}
	}
	isContainer := false
	if _, err := os.Stat("/.dockerenv"); err == nil {
		isContainer = true
	}
	isKubernetes := false

	return SystemInfo{
		Hostname:      hostname,
		IPAddress:     ip,
		IsContainer:   isContainer,
		IsKubernetes: isKubernetes,
	}
}

func getRecommendationStatus(c *gin.Context) {
	// Here you would typically check some aspects of your service to determine its status.
	// If everything's ok, return operational. Otherwise, return a different status.
	// This is a simple example without real checks, adjust according to your needs.

	// Example checks might include:
	// - Database connectivity
	// - External API/service availability
	// - Disk space, memory usage, etc.

	status := "operational"  // or "down", "maintenance", etc.

	c.JSON(http.StatusOK, gin.H{
		"status": status,
	})
}


func renderHomePage(c *gin.Context) {
	config, err := loadConfig()
	if err != nil {
		c.String(http.StatusInternalServerError, "Internal Server Error")
		return
	}
    
	systemInfo := GetSystemInfo()

	c.HTML(http.StatusOK, "index.html", gin.H{
		"Year":        time.Now().Year(),
		"Version":     config.Version,
		"SystemInfo":  systemInfo,
	})
}


func main() {
	router := gin.Default()
		
	// Load HTML files
	router.LoadHTMLGlob("templates/*")

	// Set path to serve static files
	router.Static("/static", "./static")

	// Define route for the home page
	router.GET("/", renderHomePage)

	// Handle requests to the /origami-of-the-day endpoint with the GetOrigamiOfTheDay function from the api package
	router.GET("/api/origami-of-the-day", api.GetOrigamiOfTheDay)
        
	// Service Status Page
        router.GET("/api/recommendation-status", getRecommendationStatus)


	// Start the server on port 8080
	router.Run(":8080")

}


