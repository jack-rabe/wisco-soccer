const express = require('express');
const router = express.Router();
let {PythonShell} = require('python-shell')

router.get('/schedule', (req, res) => {
  teamName = req.query.teamName
  year = req.query.year
  if (!year || !teamName){
    res.send('Either no team or year was entered.')
		return
  }
  
  const options = {mode: 'json', args: [teamName, year]}
	PythonShell.run('./scraping/schedules.py', options, (err, results) => {
    if (err) throw err
    res.json(results)
	})
});

module.exports = router;
