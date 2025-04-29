package com.example.voting.service;

import com.example.voting.config.AppProperties;
import com.example.voting.model.Origami;
import com.example.voting.repository.OrigamiRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import java.util.Collections;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

@Service
public class OrigamiSynchronizationService {

    private static final Logger log = LoggerFactory.getLogger(OrigamiSynchronizationService.class);

    @Autowired
    private OrigamiRepository origamiRepository;

    @Autowired
    private RestTemplate restTemplate;

    private final String catalogueServiceUrl;

    public OrigamiSynchronizationService(OrigamiRepository origamiRepository, RestTemplate restTemplate, AppProperties appProperties) {
        this.origamiRepository = origamiRepository;
        this.restTemplate = restTemplate;
        this.catalogueServiceUrl = appProperties.getServiceUrl();
    }

    @Scheduled(fixedRate = 60000) // 1 minute = 60000 ms
    public void synchronizeOrigamis() {
    try {
        List<Origami> origamis = fetchOrigamisFromCatalogueService();
        for (Origami origami : origamis) {
            if (origami.getOrigamiId() != null) { // Check if ID is not null
                Optional<Origami> existingOrigami = origamiRepository.findById(origami.getOrigamiId());
                if (!existingOrigami.isPresent()) {
                    origamiRepository.save(origami);
                } else {
                    Origami updatedOrigami = existingOrigami.get();
                    updatedOrigami.setName(origami.getName());
                    // updatedOrigami.setVotes(origami.getVotes());
                    origamiRepository.save(updatedOrigami);
                }
            } else {
                log.warn("Skipped Origami with null ID");
            }
        }
    } catch (Exception e) {
        log.error("Error during synchronization of origamis: " + e.getMessage(), e);
    }
    }


    private List<Origami> fetchOrigamisFromCatalogueService() {
    try {
        Origami[] origamisArray = restTemplate.getForObject(catalogueServiceUrl, Origami[].class);
        List<Origami> origamis = Arrays.asList(origamisArray);
        origamis.forEach(origami -> log.info("Fetched Origami with ID: {}", origami.getOrigamiId()));  // Log each ID
        return origamis;
    } catch (RestClientException e) {
        log.error("Failed to fetch origamis from catalogue service: " + e.getMessage(), e);
        return Collections.emptyList();
    }
    }

}

