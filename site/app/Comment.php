<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    protected $fillable = ['username', 'body', 'rating'];


    public function recipe() {
        return $this->belongsTo(Recipe::class);
    }
}
