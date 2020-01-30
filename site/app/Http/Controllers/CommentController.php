<?php

namespace App\Http\Controllers;

use App\Comment;
use App\Recipe;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class CommentController extends Controller
{
    public function save(Request $request) {

        // I really should get some actual auth
        if (!Hash::check($request['password'], '$2y$10$y/TJW50eL4loeni.h7ddv.isQZ8SDutOuhst8XGyDm2cuCxRHpb1q')) {
            return "Invalid Pass";
        }

        $vowels = ['a','e','i','o','u'];
        $requestData = $request->all();

        // Replace vowels with other vowels because I dont want to accidentally generate someone's real name
        $requestData['username'] = preg_replace("/([aeiou])/i", $vowels[array_rand($vowels)], $request->username);



        $comment = Comment::make($requestData);

        if (isset($requestData['recipe_id'])) {
            $recipe = Recipe::find($requestData['recipe_id']);
        }else{
            $recipe = Recipe::inRandomOrder()->first();
        }

        if(!$recipe){
            return "Recipe not found";
        }

        $comment->recipe()->associate($recipe)->save();

        return $comment;
    }
}
