import org.springframework.boot.web.servlet.error.ErrorController;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;
import javax.servlet.RequestDispatcher;
import javax.servlet.http.HttpServletRequest;

@Controller
public class CustomErrorController implements ErrorController {

    @RequestMapping("/error")
    public ModelAndView handleError(HttpServletRequest request) {
        Object status = request.getAttribute(RequestDispatcher.ERROR_STATUS_CODE);
        ModelAndView modelAndView = new ModelAndView("error");
        if (status != null) {
            int statusCode = Integer.parseInt(status.toString());
            switch (HttpStatus.valueOf(statusCode)) {
                case NOT_FOUND:
                    modelAndView.addObject("message", "The requested page was not found.");
                    break;
                case INTERNAL_SERVER_ERROR:
                    modelAndView.addObject("message", "An internal server error occurred.");
                    break;
                case SERVICE_UNAVAILABLE:
                    modelAndView.addObject("message", "The service is currently unavailable.");
                    break;
                default:
                    modelAndView.addObject("message", "An unexpected error has occurred.");
                    break;
            }
        }
        return modelAndView;
    }
}

