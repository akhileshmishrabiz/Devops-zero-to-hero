package com.example.voting.repository;

import com.example.voting.model.Origami;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrigamiRepository extends JpaRepository<Origami, Long> {
  int countByOrigamiId(Long origamiId);
}

