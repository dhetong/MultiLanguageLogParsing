def insert_to_dict(key, dict):
    if key in dict:
        dict[key] = dict[key] + 1
    else:
        dict[key] = 1
    return dict

def dict_builder(tokenslist, token_dict, forward_dict, backward_dict):
    token_dict = {}
    forward_dict = {}
    backward_dict = {}

    for tokens in tokenslist:
        index = 0
        while(index < len(tokens)):
            if(index == 0):
                single_token = tokens[index]
                forward_gram = tokens[index] + '->' + tokens[index+1]

                token_dict = insert_to_dict(single_token, token_dict)
                forward_dict = insert_to_dict(forward_gram, forward_dict)
            elif(index == len(tokens)-1):
                single_token = tokens[index]
                backward_gram = tokens[index] + '<-' + tokens[index-1]

                token_dict = insert_to_dict(single_token, token_dict)
                backward_dict = insert_to_dict(backward_gram, backward_dict)
            else:
                single_token = tokens[index]
                forward_gram = tokens[index] + '->' + tokens[index+1]
                backward_gram = tokens[index] + '<-' + tokens[index - 1]

                token_dict = insert_to_dict(single_token, token_dict)
                forward_dict = insert_to_dict(forward_gram, forward_dict)
                backward_dict = insert_to_dict(backward_gram, backward_dict)
            index = index+1

    return token_dict, forward_dict, backward_dict

def compund_combiner(tokens, token_dict, forward_dict, backward_dict, threshold):
    combine_pos = []
    index = 0
    while(index < len(tokens)):
        if(index == 0):
            single_token = tokens[index]
            forward_gram = tokens[index] + '->' + tokens[index + 1]

            possbility_forward = forward_dict[forward_gram]/token_dict[single_token]
            if(possbility_forward > threshold):
                combine_pos.append(index)
        elif(index == len(tokens)-1):
            single_token = tokens[index]
            backward_gram = tokens[index] + '<-' + tokens[index - 1]

            possbility_backward = backward_dict[backward_gram]/token_dict[single_token]
            if(possbility_backward > threshold):
                combine_pos.append(index-1)
        else:
            single_token = tokens[index]
            forward_gram = tokens[index] + '->' + tokens[index + 1]
            backward_gram = tokens[index] + '<-' + tokens[index - 1]

            possbility_forward = forward_dict[forward_gram] / token_dict[single_token]
            possbility_backward = backward_dict[backward_gram] / token_dict[single_token]
            if (possbility_forward > threshold):
                combine_pos.append(index)
            if (possbility_backward > threshold):
                combine_pos.append(index-1)
        index = index+1

    index = 0
    tokens_new = []
    tokens_new.append(tokens[0])
    while(index < len(tokens)-2):
        if(index in combine_pos):
            tokens_new[len(tokens_new)-1] = tokens_new[len(tokens_new)-1] + tokens[index+1]
        else:
            tokens_new.append(tokens[index+1])
        index = index+1

    return tokens_new