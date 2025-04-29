package com.example.voting.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.example.voting.model.Origami;
import com.example.voting.repository.OrigamiRepository;

import java.util.Optional;

@Service
public class OrigamiService {

    @Autowired
    private OrigamiRepository origamiRepository;

    public Optional<Origami> getOrigamiById(Long id) {
        return origamiRepository.findById(id);
    }

    public Origami saveOrUpdateOrigami(Origami origami) {
        return origamiRepository.save(origami);
    }

    public int getVotes(Long origamiId) {
        return origamiRepository.findById(origamiId)
                .map(Origami::getVotes)  // Assuming getVotes() method exists in Origami model
                .orElse(0);  // Return 0 if the origami is not found
    }
}
