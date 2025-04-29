package com.example.voting.model;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import lombok.Data;
import com.fasterxml.jackson.annotation.JsonProperty;

@Data
@Entity
public class Origami {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long origamiId;
    private String name;
    private int votes;

    @JsonProperty("id")  // Ensure that this maps the 'id' from JSON to 'origamiId'
    public void setOrigamiId(Long id) {
        this.origamiId = id;
    }

    // No need for any conversion now since the IDs are already in the correct format (Long)
}

