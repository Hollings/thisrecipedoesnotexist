<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class AddQueuedRecipesTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('queued_recipes', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->unsignedInteger('recipe_id')->nullable();
            $table->string('requested_by_name');
            $table->string('requested_by_id');
            $table->string('mention_id');
            $table->string('title');
            $table->string('status');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::drop('queued_recipes');
    }
}
