const mongoose = require("mongoose");

const pingStatusSchema = new mongoose.Schema(
    {
        
    },
    {
        timestamp: true,
    }
)

/*
ID Number

Location Name

Pi IP address

Average Latency

Number of failed pings

Number of total pings
*/

/*
Reply from 8.8.8.8: bytes=32 time=68ms TTL=115
*/
