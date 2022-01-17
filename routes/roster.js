const express = require('express');
const router = express.Router();
let {PythonShell} = require('python-shell')

router.post('/', (req, res) => {
  teamName = req.body.teamName
  year = req.body.year
  if (!year || !teamName){
    res.send('Either no team or year was entered.')
  }
  
  const options = {mode: 'json', args: [teamName, year]}
	PythonShell.run('./scraping/rosters.py', options, (err, results) => {
    if (err) throw err
    res.json(results)
	})
});

module.exports = router;
