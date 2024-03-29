from diffusers import StableDiffusionPipeline
import argparse, os, json
import torch

def parse_args():
    parser = argparse.ArgumentParser(description="generating images using the frozen pretrained diffusion model")

    parser.add_argument(
        "--num_per_epoch",
        type=int,
        default=1,
        required=False,
        help="How many images are simple_generated in one epoch",
    )

    parser.add_argument(
        "--model_path",
        type=str,
        default="../log/saved_models/pink_sunglasses",
        required=False,
        help="the pretrained checkpoint path",
    )

    parser.add_argument(
        "--eval_file",
        type=str,
        default="../data/eval.txt",
        required=False,
        help="the path where prompt json is stored",
    )

    parser.add_argument(
        "--img_path",
        type=str,
        default='../data/img/eval_1000',
        required=False,
        help="the path where class json is stored",
    )

    parser.add_argument(
        '--subject',
        type=str,
        default='red_cartoon',
        help='The subject id',
    )

    parser.add_argument(
        '--identifier',
        type=str,
        default='ZIdNKNNC',
        help='The identifier',
    )

    parser.add_argument(
        '--checkpoint_list',
        nargs='+',
        type=str,
        default=['325', '350', '400', '450', '525'],
        help='The subject id',
    )

    args = parser.parse_args()
    os.makedirs(args.img_path, exist_ok=True)
    return args

n_samples, scale, steps = 8, 7.5, 500

if __name__ == '__main__':
    config = parse_args()

    eval_list = json.load(open(config.eval_json, 'r'))
    eval_list = [s.replace('[V]', config.identifier) for s in eval_list[config.subject]]

    for check_point_id in config.checkpoint_list:
        check_point_path = os.path.join(config.model_path, f'saved_model_{check_point_id}')
        pipe = StableDiffusionPipeline.from_pretrained(check_point_path, torch_dtype=torch.float32)
        pipe = pipe.to("cuda")

        save_path = os.path.join(config.img_path, config.subject, check_point_id)
        os.makedirs(save_path, exist_ok=True)

        for prompt in eval_list:
            images = pipe(prompt, guidance_scale=scale, num_inference_steps=steps, num_images_per_prompt=n_samples).images

            for idx, im in enumerate(images):
                im.save(f"{save_path}/{prompt}_{idx:02}.png")

        del pipe
