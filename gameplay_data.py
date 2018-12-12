class Gameplay_Data(object):
    
    ##################
    ## Constructors ##
    ##################
    def __init__(self, total_deaths, deaths_through_gaps, deaths_through_opponents):
        
        self.total_deaths = total_deaths
        self.deaths_through_gaps = deaths_through_gaps
        self.deaths_through_opponents = deaths_through_opponents

    #############
    ## Getters ##
    #############
    def get_total_deaths(self):

        return self.total_deaths

    def get_deaths_through_gaps(self):

        return self.deaths_through_gaps

    def get_deaths_through_opponents(self):

        return self.deaths_through_opponents

    #############
    ## Setters ##
    #############

    def set_total_deaths(self, total_deaths):
    
        self.total_deaths = total_deaths

    def set_deaths_through_gaps(self, deaths_through_gaps):

        self.deaths_through_gaps = deaths_through_gaps

    def set_deaths_through_opponents(self, deaths_through_opponents):

        self.deaths_through_opponents = deaths_through_opponents