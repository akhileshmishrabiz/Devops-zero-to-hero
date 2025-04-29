const express = require('express');
const axios = require('axios');
const router = express.Router();

// Voting Service base URL
const VOTING_SERVICE_BASE_URL = 'http://voting:8080';

// Vote for an Origami
router.post('/:origamiId/vote', async (req, res, next) => {
    try {
        await axios.post(`${VOTING_SERVICE_BASE_URL}/api/origamis/${req.params.origamiId}/vote`);
        res.status(200).send('Vote recorded!');
    } catch (error) {
        console.error('Error voting:', error);
        res.status(500).send('Internal Server Error');
    }
});

// Get vote count for an Origami
router.get('/:origamiId/votes', async (req, res, next) => {
    try {
        const response = await axios.get(`${VOTING_SERVICE_BASE_URL}/api/origamis/${req.params.origamiId}/votes`);
        res.status(200).json(response.data);
    } catch (error) {
        console.error('Error fetching vote count:', error);
        res.status(500).send('Internal Server Error');
    }
});

module.exports = router;

