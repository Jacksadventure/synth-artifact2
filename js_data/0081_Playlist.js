// Creating models
// Step1: Require Mongoose

const mongoose = require ("mongoose");

// Step2: Create Schema --> This defines how the user data structure will look like

const Playlist = mongoose.Schema({
    name:{
        type: String,
        required: true
    },
    thumbnail:{
        type: String,
        required: false
    },
    owner:{
        type: mongoose.Types.ObjectId,
        ref: "User",
        required: false
    },
    songs: [{
        type: mongoose.Types.ObjectId,
        ref: "Song",
        required: true
    }],
    collaborators: [{
        type: mongoose.Types.ObjectId,
        ref: "User",
        required: false
    }]
});

// Step3: Create Model --> This defines how the data will be stored in the database

const PlaylistModel = mongoose.model("Playlist", Playlist);

module.exports = PlaylistModel;