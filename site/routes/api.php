<?php

use Illuminate\Http\Request;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::post('add', 'RecipeController@saveRecipe');
Route::post('comment/add', 'CommentController@save');

Route::post('queue', 'RecipeController@queueRecipe');
Route::get('recipe', 'RecipeController@getRecipeRaw');
Route::get('search','RecipeController@search');
Route::get('queue','RecipeController@getNextQueuedRecipe');